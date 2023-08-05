from setuptools import setup

setup(
    name='pystatistic',# 需要打包的名字,即本模块要发布的名字
    version='v1.0',#版本
    description='Count every thing!', # 简要描述
    py_modules=['pystatistic.pystatistic'],   #  需要打包的模块
    author='DY_XiaoDong', # 作者名
    author_email='xiaodong@indouyin.cn',   # 作者邮件
    url='https://xiaodong.indouyin.cn/python/modules/pystatistic/index.html', # 项目地址,一般是代码托管的网站
    requires=['colorama'], # 依赖包
    install_requires=['colorama'], # 强制下载的依赖包
    license='MIT'
)
