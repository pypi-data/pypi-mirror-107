# coding=utf-8
from sdk import *


def test_add_log_ConsoleConsumer():
    # 打印日志
    consumer = ConsoleConsumer()
    # 使用 Consumer 来构造 NifflerAnalytics 对象
    niffer = NifflerAnalytics(consumer, project_name='production')
    properties = {
        'id': 1,
        'name': 'test',
        'age': '10',
        'addr': '北京',
        'time': datetime.datetime.now()

    }
    niffer.add_log(log_type="es", properties=properties)
    niffer.close()


def test_add_log_LoggingConsumer():
    # 打印日志
    # log_name 为log存储的绝对路径+log名称，此路径与filebeat中的配置文件paths要一致
    log_name = "data0/logs/event1.log"
    consumer = LoggingConsumer(log_name)
    # 使用 Consumer 来构造 NifflerAnalytics 对象
    niffer = NifflerAnalytics(consumer, project_name='production')
    properties = {
        'id': 1,
        'name': 'test',
        'age': '10',
        'addr': '北京',
        'time': datetime.date.today()

    }
    niffer.add_log(log_type="es", properties=properties)
    niffer.close()


def test_add_log_ConcurrentLoggingConsumer():
    # 打印日志
    # log_name 为log存储的绝对路径+log名称，此路径与filebeat中的配置文件paths要一致
    log_name = "/data0/logs/event.log"
    consumer = ConcurrentLoggingConsumer(log_name)
    # 使用 Consumer 来构造 NifflerAnalytics 对象
    niffer = NifflerAnalytics(consumer, project_name='production')
    properties = {
        'id': 1,
        'name': 'test',
        'age': '10',
        'addr': '北京',
        'time': datetime.date.today()

    }
    niffer.add_log(log_type="", properties=properties)
    niffer.close()


def test_add_event_ConsoleConsumer():
    # 打印日志
    consumer = ConsoleConsumer()
    # 使用 Consumer 来构造 NifflerAnalytics 对象
    niffer = NifflerAnalytics(consumer, project_name='production')
    properties = {
        'name': 'test_add_event_ConcurrentLoggingConsumer',
        'age': '10',
        'addr': u'北京',
        'now': datetime.date.today()

    }
    distinct_id = '123456'
    event_type = "order"
    event_name = "woman_order"
    niffer.add_event(distinct_id, event_type, event_name, properties)

    niffer.close()


def test_add_event_LoggingConsumer():
    # 打印日志
    # log_name 为log存储的绝对路径+log名称，此路径与filebeat中的配置文件paths要一致
    log_name = "/data0/logs/event1.log"
    consumer = LoggingConsumer(log_name)
    # 使用 Consumer 来构造 NifflerAnalytics 对象
    niffer = NifflerAnalytics(consumer, project_name='production')
    properties = {
        'name': 'test_add_event_LoggingConsumer',
        'age': '10',
        'addr': u'北京',
        'now': datetime.date.today()
    }
    distinct_id = '123456'
    event_type = "order"
    event_name = "woman_order"
    niffer.add_event(distinct_id, event_type, event_name, properties)
    niffer.close()


def test_add_event_ConcurrentLoggingConsumer():
    # 打印日志
    # log_name 为log存储的绝对路径+log名称，此路径与filebeat中的配置文件paths要一致
    log_name = "/data0/logs/event2.log"
    consumer = ConcurrentLoggingConsumer(log_name, encoding='utf-8')
    # 使用 Consumer 来构造 NifflerAnalytics 对象
    niffer = NifflerAnalytics(consumer, project_name='production')
    properties = {
        'name': 'test_add_event_ConcurrentLoggingConsumer',
        'age': '10',
        'addr': u'北京',
        'now': datetime.date.today()

    }
    distinct_id = '123456'
    event_type = "order"
    event_name = "woman_order"
    niffer.add_event(distinct_id, event_type, event_name, properties)
    niffer.close()


if __name__ == '__main__':
    # test_add_log_ConsoleConsumer()
    # test_add_log_LoggingConsumer()
    test_add_log_ConcurrentLoggingConsumer()

    # test_add_event_ConsoleConsumer()
    # test_add_event_LoggingConsumer()
    test_add_event_ConcurrentLoggingConsumer()
