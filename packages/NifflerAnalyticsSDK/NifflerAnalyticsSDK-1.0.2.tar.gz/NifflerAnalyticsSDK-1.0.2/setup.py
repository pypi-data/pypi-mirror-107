import setuptools

#  打包: python setup.py sdist
#  对包进行检查: twine check dist/*
#  运行上传: twine upload dist/* --config-file .pypirc


# 读取项目的readme介绍
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="NifflerAnalyticsSDK",
    version="1.0.2",
    author="ShiKun",  # 项目作者
    author_email="429143597@qq.com",
    description="This is the official Python SDK for Niffler Analytics.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://code.yidianshihui.com/j.a.r.v.i.s/niffer-python",
    packages=setuptools.find_packages(),
)
