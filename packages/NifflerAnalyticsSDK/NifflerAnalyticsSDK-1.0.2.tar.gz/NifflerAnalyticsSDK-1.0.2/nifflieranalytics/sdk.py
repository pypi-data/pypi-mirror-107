# coding=utf-8

from __future__ import unicode_literals

import base64
import datetime
import gzip
import json
import logging
import logging.handlers
import os
import re
import threading
import time
import traceback
import uuid

from numpy import long
from pyparsing import basestring

try:
    from urllib.parse import urlparse
    import queue
    import urllib.parse as urllib
    import urllib.request as urllib2
except ImportError:
    from urlparse import urlparse
    import Queue as queue
    import urllib2
    import urllib

SDK_VERSION = '1.0.2'
batch_consumer_lock = threading.RLock()

try:
    isinstance("", basestring)


    def is_str(s):
        return isinstance(s, basestring)
except NameError:
    def is_str(s):
        return isinstance(s, str)

try:
    isinstance(1, long)


    def is_int(n):
        return isinstance(n, int) or isinstance(n, long)
except NameError:
    def is_int(n):
        return isinstance(n, int)


class NifflerAnalyticsException(Exception):
    pass


class NifflerAnalyticsIllegalDataException(NifflerAnalyticsException):
    """
    在发送的数据格式有误时，SDK会抛出此异常，用户应当捕获并处理。
    """
    pass


class NifflerAnalyticsNetworkException(NifflerAnalyticsException):
    """
    在因为网络或者不可预知的问题导致数据无法发送时，SDK会抛出此异常，用户应当捕获并处理。
    """
    pass


class NifflerAnalyticsFileLockException(NifflerAnalyticsException):
    """
    当 ConcurrentLoggingConsumer 文件锁异常时，SDK 会抛出此异常，用户应当捕获并记录错误日志。
    """
    pass


class NifflerAnalyticsDebugException(Exception):
    """
    Debug模式专用的异常
    """
    pass


if os.name == 'nt':  # pragma: no cover
    import msvcrt


    def lock(file_):
        try:
            savepos = file_.tell()

            file_.seek(0)

            try:
                msvcrt.locking(file_.fileno(), msvcrt.LK_LOCK, 1)
            except IOError as e:
                raise NifflerAnalyticsFileLockException(e)
            finally:
                if savepos:
                    file_.seek(savepos)
        except IOError as e:
            raise NifflerAnalyticsFileLockException(e)


    def unlock(file_):
        try:
            savepos = file_.tell()
            if savepos:
                file_.seek(0)

            try:
                msvcrt.locking(file_.fileno(), msvcrt.LK_UNLCK, 1)
            except IOError as e:
                raise NifflerAnalyticsFileLockException(e)
            finally:
                if savepos:
                    file_.seek(savepos)
        except IOError as e:
            raise NifflerAnalyticsFileLockException(e)

elif os.name == 'posix':  # pragma: no cover
    import fcntl


    def lock(file_):
        try:
            fcntl.flock(file_.fileno(), fcntl.LOCK_EX)
        except IOError as e:
            raise NifflerAnalyticsFileLockException(e)


    def unlock(file_):
        fcntl.flock(file_.fileno(), fcntl.LOCK_UN)

else:
    raise NifflerAnalyticsFileLockException("NifflerAnalytics SDK is defined for NT and POSIX system.")


class SAFileLock(object):

    def __init__(self, file_handler):
        self._file_handler = file_handler

    def __enter__(self):
        lock(self._file_handler)
        return self

    def __exit__(self, t, v, tb):
        unlock(self._file_handler)


class NifflerAnalytics(object):
    """
    使用一个 NifflerAnalytics 的实例来进行数据发送。
    """

    NAME_PATTERN = re.compile(
        r"^((?!^distinct_id$|^original_id$|^time$|^properties$|^id$|^first_id$|^second_id$|^users$|^events$|^event$|^user_id$|^date$|^datetime$|^type$)[a-zA-Z_$][a-zA-Z\d_$]{0,99})$",
        re.I)

    class DatetimeSerializer(json.JSONEncoder):
        """
        实现 date 和 datetime 类型的 JSON 序列化，以符合 NifflerAnalytics 的要求。
        """

        def default(self, obj):
            if isinstance(obj, datetime.datetime):
                head_fmt = "%Y-%m-%d %H:%M:%S"
                return "{main_part}.{ms_part}".format(
                    main_part=obj.strftime(head_fmt),
                    ms_part=int(obj.microsecond / 1000))
            elif isinstance(obj, datetime.date):
                fmt = '%Y-%m-%d'
                return obj.strftime(fmt)
            return json.JSONEncoder.default(self, obj)

    def __init__(self, consumer, project_name):
        """
        初始化一个 NifflerAnalytics 的实例。可以选择使用默认的 DefaultConsumer，也可以选择其它的 Consumer 实现。

        已实现的 Consumer 包括:
        DefaultConsumer: 默认实现，逐条、同步的发送数据;
        BatchConsumer: 批量、同步的发送数据;
        AsyncBatchConsumer: 批量、异步的发送数据;
        DebugConsumer:专门用于调试，逐条、同步地发送数据到专用的Debug接口，并且如果数据有异常会退出并打印异常原因

        @param consumer SDK实例使用的Consumer
        @param project_name Project名称
        """
        self._consumer = consumer
        self._default_project_name = project_name
        self._super_properties = {}
        self.clear_super_properties();

    @staticmethod
    def _now():
        return int(time.time() * 1000)

    @staticmethod
    def _json_dumps(data):
        return json.dumps(data, separators=(',', ':'), cls=NifflerAnalytics.DatetimeSerializer)

    def register_super_properties(self, super_properties):
        """
        设置每个事件都带有的一些公共属性，当 track 的 properties 和 super properties 有相同的 key 时，将采用 track 的

        :param super_properties 公共属性
        """
        self._super_properties.update(super_properties)

    def clear_super_properties(self):
        """
        删除所有已设置的事件公共属性
        """
        self._super_properties = {
            '$lib': 'python',
            '$lib_version': SDK_VERSION,
        }

    def add_event(self, distinct_id, event_type, event_name, properties):
        """
        跟踪一个用户的行为。
        :param distinct_id: 用户的唯一标识
        :param event_type: 事件类型 不传的话，则只做日志落盘本地，不会通过filebeat传递至kafka
        :param event_name: 事件名称
        :param properties: 事件的属性
        :param distinct_id:
        :return:
        """
        self._track_event(event_type, event_name, distinct_id, properties)

    def add_log(self, log_type, properties):
        """
        添加日志，日志落盘本地，并通过filebeat传递至kafka做二次处理
        :param log_type: log类型，不传的话，则只做日志落盘本地，不会通过filebeat传递至kafka
        :param properties:
        :return:
        """
        self._track_log(log_type, properties)

    @staticmethod
    def _normalize_properties(data):
        if "properties" in data and data["properties"] is not None:
            for key, value in data["properties"].items():
                if not is_str(key):
                    raise NifflerAnalyticsIllegalDataException("property key must be a str. [key=%s]" % str(key))
                if len(key) > 255:
                    raise NifflerAnalyticsIllegalDataException(
                        "the max length of property key is 256. [key=%s]" % str(key))
                if not NifflerAnalytics.NAME_PATTERN.match(key):
                    raise NifflerAnalyticsIllegalDataException(
                        "property key must be a valid variable name. [key=%s]" % str(key))

                if is_str(value) and len(value) > 8191:
                    raise NifflerAnalyticsIllegalDataException(
                        "the max length of property key is 8192. [key=%s]" % str(key))

                if not is_str(value) and not is_int(value) and not isinstance(value, float) \
                        and not isinstance(value, datetime.datetime) and not isinstance(value, datetime.date) \
                        and not isinstance(value, list) and value is not None:
                    raise NifflerAnalyticsIllegalDataException(
                        "property value must be a str/int/float/datetime/date/list. [value=%s]" % type(value))
                if isinstance(value, list):
                    for lvalue in value:
                        if not is_str(lvalue):
                            raise NifflerAnalyticsIllegalDataException(
                                "[list] property's value must be a str. [value=%s]" % type(lvalue))

    @staticmethod
    def _normalize_data(data):
        # 检查 distinct_id
        if data["distinct_id"] is None or len(str(data['distinct_id'])) == 0:
            raise NifflerAnalyticsIllegalDataException("property [distinct_id] must not be empty")
        if len(str(data['distinct_id'])) > 255:
            raise NifflerAnalyticsIllegalDataException("the max length of property [distinct_id] is 255")
        data['distinct_id'] = str(data['distinct_id'])

        # 检查 time
        if isinstance(data['time'], datetime.datetime):
            data['time'] = time.mktime(data['time'].timetuple()) * 1000 + data['time'].microsecond / 1000

        ts = int(data['time'])
        ts_num = len(str(ts))
        if ts_num < 10 or ts_num > 13:
            raise NifflerAnalyticsIllegalDataException("property [time] must be a timestamp in microseconds")

        if ts_num == 10:
            ts *= 1000
        data['time'] = ts

        # 检查 Event Name
        if 'event' in data and not NifflerAnalytics.NAME_PATTERN.match(data['event']):
            raise NifflerAnalyticsIllegalDataException(
                "event name must be a valid variable name. [name=%s]" % data['event'])

        # 检查 Event Name
        if 'project_name' in data and not NifflerAnalytics.NAME_PATTERN.match(data['project_name']):
            raise NifflerAnalyticsIllegalDataException(
                "project name must be a valid variable name. [project_name=%s]" % data['project_name'])

        # 检查 Event Name
        if 'type' in data and not NifflerAnalytics.NAME_PATTERN.match(data['type']):
            raise NifflerAnalyticsIllegalDataException(
                "log type must be a valid variable name. [log_type=%s]" % data['type'])

        # 检查 properties
        NifflerAnalytics._normalize_properties(data)
        return data

    def _get_lib_properties(self):
        lib_properties = {
            '$lib': 'python',
            '$lib_version': SDK_VERSION,
            '$lib_method': 'code',
        }

        if '$app_version' in self._super_properties:
            lib_properties['$app_version'] = self._super_properties['$app_version']

        try:
            raise Exception
        except:
            trace = traceback.extract_stack(limit=5)
            if len(trace) > 3:
                try:
                    file_name = trace[-4][0]
                    line_number = trace[-4][1]

                    if trace[-4][2].startswith('<'):
                        function_name = ''
                    else:
                        function_name = trace[-4][2]

                    try:
                        if len(trace) > 4 and trace[-5][3]:
                            class_name = trace[-5][3].split('(')[0]
                        else:
                            class_name = ''
                    except:
                        print(trace.format())

                    lib_properties['$lib_detail'] = '%s##%s##%s##%s' % (
                        class_name, function_name, file_name, line_number)
                except:
                    pass

        return lib_properties

    def _get_common_properties(self):
        """
        构造所有 Event 通用的属性:
        """
        common_properties = {
            '$lib': 'python',
            '$lib_version': SDK_VERSION,
        }

        if self._app_version:
            common_properties['$app_version'] = self._app_version

        return common_properties

    @staticmethod
    def _extract_user_time(properties):
        """
        如果用户传入了 $time 字段，则不使用当前时间。
        """
        if properties is not None and '$time' in properties:
            t = properties['$time']
            del (properties['$time'])
            return t
        return None

    @staticmethod
    def _extract_token(properties):
        """
        如果用户传入了 $token 字段，则在 properties 外层加上token，并删除 $token 字段
        """
        if properties is not None and '$token' in properties:
            t = properties['$token']
            del (properties['$token'])
            return t
        return None

    @staticmethod
    def _extract_project(properties):
        """
        如果用户传入了 $project 字段，则在 properties 外层加上 project，并删除 $project 字段
        """
        if properties is not None and '$project_name' in properties:
            t = properties['$project_name']
            del (properties['$project_name'])
            return t
        return None

    @staticmethod
    def _normalize_item_data(data):
        # 检查 item_type
        if not NifflerAnalytics.NAME_PATTERN.match(data['item_type']):
            raise NifflerAnalyticsIllegalDataException(
                "item_type must be a valid variable name. [key=%s]" % str(data['item_type']))

        # 检查 item_id
        if data['item_id'] is None or len(str(data['item_id'])) == 0:
            raise NifflerAnalyticsIllegalDataException("item_id must not be empty")
        if len(str(data['item_id'])) > 255:
            raise NifflerAnalyticsIllegalDataException("the max length of item_id is 255")
        # 检查 properties
        NifflerAnalytics._normalize_properties(data)
        return data

    def _track_item(self, event_type, item_type, item_id, properties):
        if properties is None:
            properties = {}
        data = {
            'type': event_type,
            'time': self._now(),
            'lib': self._get_lib_properties(),
            'item_type': item_type,
            'item_id': item_id,
        }

        if self._default_project_name is not None:
            data['project_name'] = self._default_project_name

        if properties and '$project_name' in properties and len(str(properties['$project_name'])) != 0:
            data['project_name'] = properties['$project_name']
            properties.pop('$project_name')

        data['properties'] = properties

        data = self._normalize_item_data(data)
        self._json_dumps(data)
        self._consumer.send(self._json_dumps(data))

    @staticmethod
    def _gen_event_id():
        event_id = str(uuid.uuid1()).replace('-', '')
        return event_id

    def _track_event(self, event_type, event_name, distinct_id, properties):
        event_time = self._extract_user_time(properties) or self._now()

        data = {
            'type': event_type,
            'time': event_time,
            'distinct_id': distinct_id,
            'properties': properties,
            'lib': self._get_lib_properties(),
            'event_id': self._gen_event_id(),
            'project_name': self._default_project_name,
            'event': event_name,
        }

        data = self._normalize_data(data)
        self._consumer.send(self._json_dumps(data))

    def _track_log(self, log_type, properties):
        event_time = self._extract_user_time(properties) or self._now()

        data = {
            'time': event_time,
            'properties': properties,
            'log_id': self._gen_event_id(),
            'project_name': self._default_project_name,
        }
        if log_type != "":
            data['type'] = log_type

        self._consumer.send(self._json_dumps(data))

    def flush(self):
        """
        对于不立即发送数据的 Consumer，调用此接口应当立即进行已有数据的发送。
        """
        self._consumer.flush()

    def close(self):
        """
        在进程结束或者数据发送完成时，应当调用此接口，以保证所有数据被发送完毕。
        如果发生意外，此方法将抛出异常。
        """
        self._consumer.close()


class DebugConsumer(object):
    """
    调试用的 Consumer，逐条发送数据到服务器的Debug API,并且等待服务器返回的结果
    具体的说明在http://www.Nifflerdata.cn/manual/
    """

    def __init__(self, url_prefix, write_data=True, request_timeout=None):
        """
        初始化Consumer
        :param url_prefix: 服务器提供的用于Debug的API的URL地址,特别注意,它与导入数据的API并不是同一个
        :param write_data: 发送过去的数据,是真正写入,还是仅仅进行检查
        :param request_timeout:请求的超时时间,单位为秒
        :return:
        """
        debug_url = urlparse(url_prefix)
        ## 将 URI Path 替换成 Debug 模式的 '/debug'
        debug_url = debug_url._replace(path='/debug')

        self._debug_url_prefix = debug_url.geturl()
        self._request_timeout = request_timeout
        self._debug_write_data = write_data

    @staticmethod
    def _gzip_string(data):
        try:
            return gzip.compress(data)
        except AttributeError:
            import StringIO

            buf = StringIO.StringIO()
            fd = gzip.GzipFile(fileobj=buf, mode="w")
            fd.write(data)
            fd.close()
            return buf.getvalue()

    def _do_request(self, data):
        """
        使用 urllib 发送数据给服务器，如果发生错误会抛出异常。
        response的结果,会返回
        """
        encoded_data = urllib.urlencode(data).encode('utf8')
        try:
            request = urllib2.Request(self._debug_url_prefix, encoded_data)
            if not self._debug_write_data:  # 说明只检查,不真正写入数据
                request.add_header('Dry-Run', 'true')
            if self._request_timeout is not None:
                response = urllib2.urlopen(request, timeout=self._request_timeout)
            else:
                response = urllib2.urlopen(request)
        except urllib2.HTTPError as e:
            return e
        return response

    def send(self, msg):
        response = self._do_request({
            'data': self._encode_msg(msg),
            'gzip': 1
        })
        print('==========================================================================')
        ret_code = response.code
        if ret_code == 200:
            print('valid message: %s' % msg)
        else:
            print('invalid message: %s' % msg)
            print('ret_code: %s' % ret_code)
            print('ret_content: %s' % response.read().decode('utf8'))
        if ret_code >= 300:
            raise NifflerAnalyticsDebugException()

    def _encode_msg(self, msg):
        return base64.b64encode(self._gzip_string(msg.encode('utf8')))

    def flush(self):
        pass

    def close(self):
        pass


class ConsoleConsumer(object):
    """
    将数据直接输出到标准输出
    """

    def __init__(self):
        pass

    @staticmethod
    def send(msg):
        print(msg)

    def flush(self):
        pass

    def close(self):
        pass


class LoggingConsumer(object):
    """
    将数据使用 logging 库输出到指定路径，并默认按天切割
    log_name 为log存储的绝对路径+log名称，此路径与filebeat中的配置文件paths要一致
    如果只想日志存储到本地，不通过filebeat传递至后端，可不将日志路径添加在filebeat配置文件的paths中
    """

    def __init__(self, log_name, backupCount=0, when='midnight', encoding=None):
        log_handler = logging.handlers.TimedRotatingFileHandler(log_name, when=when, backupCount=backupCount, encoding=encoding)
        log_handler.setFormatter(logging.Formatter('%(message)s'))
        self.logger = logging.getLogger('NifflerAnalyticsLogger')
        self.logger.propagate = False
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(log_handler)

    def send(self, msg):
        self.logger.info(msg)

    def flush(self):
        self.logger.handlers[0].flush()

    def close(self):
        self.logger.handlers[0].close()


class ConcurrentLoggingConsumer(object):
    """
    将数据输出到指定路径，并按天切割，支持多进程并行输出到同一个文件名
    log_name 为log存储的绝对路径+log名称，此路径与filebeat中的配置文件paths要一致
    如果只想日志存储到本地，不通过filebeat传递至后端，可不将日志路径添加在filebeat配置文件的paths中
    """

    class ConcurrentFileWriter(object):

        def __init__(self, filename, encoding=None):
            self._filename = filename
            self._file = open(filename, 'a', encoding=encoding)

        def close(self):
            self._file.close()

        def isValid(self, filename):
            return self._filename == filename

        def write(self, messages):
            with SAFileLock(self._file):
                for message in messages:
                    self._file.write(message)
                    self._file.write('\n')
                self._file.flush()

    @classmethod
    def construct_filename(cls, log_name):
        return log_name + '.' + datetime.datetime.now().strftime('%Y-%m-%d')

    def __init__(self, log_name, bufferSize=8192, encoding=None):
        self._log_name = log_name
        self._buffer = []
        self._bufferSize = bufferSize

        self._mutex = queue.Queue()
        self._mutex.put(1)

        self._encoding = encoding

        filename = ConcurrentLoggingConsumer.construct_filename(self._log_name)
        print(filename)
        self._writer = ConcurrentLoggingConsumer.ConcurrentFileWriter(filename, encoding=self._encoding)

    def send(self, msg):
        messages = None

        self._mutex.get(block=True, timeout=None)

        self._buffer.append(msg)

        if len(self._buffer) > self._bufferSize:
            messages = self._buffer

            filename = ConcurrentLoggingConsumer.construct_filename(self._log_name)
            if not self._writer.isValid(filename):
                self._writer.close()
                self._writer = ConcurrentLoggingConsumer.ConcurrentFileWriter(filename, encoding=self._encoding)

            self._buffer = []

        self._mutex.put(1)

        if messages:
            self._writer.write(messages)

    def flush(self):
        messages = None

        self._mutex.get(block=True, timeout=None)

        if len(self._buffer) > 0:
            messages = self._buffer

            filename = ConcurrentLoggingConsumer.construct_filename(self._log_name)
            if not self._writer.isValid(filename):
                self._writer.close()
                self._writer = ConcurrentLoggingConsumer.ConcurrentFileWriter(filename, encoding=self._encoding)

            self._buffer = []

        self._mutex.put(1)

        if messages:
            self._writer.write(messages)

    def close(self):
        self.flush()
        self._writer.close()
