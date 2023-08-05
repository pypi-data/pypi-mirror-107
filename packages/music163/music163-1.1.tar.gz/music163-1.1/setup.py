from setuptools import setup

setup(
    name='music163',# 需要打包的名字,即本模块要发布的名字
    version='v1.1',#版本
    description='Download the 163 music for free!', # 简要描述
    py_modules=['music163.music163'],   #  需要打包的模块
    author='DY_XiaoDong', # 作者名
    packages=['music163'],
    author_email='xiaodong@indouyin.cn',   # 作者邮件
    url='https://xiaodong.indouyin.cn/python/modules/music163/index.html', # 项目地址,一般是代码托管的网站
    requires=['requests','pylucky','urllib3','requests'], # 依赖包,如果没有,可以不要
    install_requires=['requests','pylucky','urllib3','requests'], # 强制下载的依赖包
    license='MIT',
)
