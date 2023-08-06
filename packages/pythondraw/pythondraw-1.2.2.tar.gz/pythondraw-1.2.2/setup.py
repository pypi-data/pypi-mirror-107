from setuptools import setup

setup(
    name='pythondraw',# 需要打包的名字,即本模块要发布的名字
    version='v1.2.2',#版本
    description='A drawing module more suitable for novices', # 简要描述
    py_modules=['pythondraw.pythondraw'],   #  需要打包的模块
    author='DY_XiaoDong', # 作者名
    packages=['pythondraw'],
    author_email='xiaodong@indouyin.cn',   # 作者邮件
    url='https://xiaodong.indouyin.cn/python/modules/pythondraw/index.html', # 项目地址,一般是代码托管的网站
    requires=['turtle'], # 依赖包,如果没有,可以不要
    license='MIT',
)
