from __future__ import print_function
from setuptools import setup, find_packages

setup(
    name="Yamler",
    version="0.0.1",
    author="ZhouHanLin",  # 作者名字
    author_email="zhhlvip@sina.com",
    description="Python parse yaml.",
    license="MIT",
    url="",  # github地址或其他地址
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Environment :: Web Environment",
        'Intended Audience :: Developers',
        'Natural Language :: Chinese (Simplified)',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Operating System :: Microsoft',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    install_requires=[
        'PyYAML>=5.4.1'  # 所需要包的版本号
    ],
    zip_safe=True,
)
