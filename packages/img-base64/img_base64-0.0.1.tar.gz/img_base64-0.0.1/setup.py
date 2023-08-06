import setuptools



setuptools.setup(
    name="img_base64", # Replace with your own username  #自定义封装模块名与文件夹名相同
    version="0.0.1", #版本号，下次修改后再提交的话只需要修改当前的版本号就可以了
    author="袁运强", #作者
    author_email="6497569033@qq.com", #邮箱
    description="调用此方法可将图片转为base64格式", #描述
    long_description='调用此方法可将图片转为base64格式', #描述
    long_description_content_type="text/markdown", #markdown
    url="https://github.com/yuanyunqiang", #github地址
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License", #License
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  #支持python版本
)