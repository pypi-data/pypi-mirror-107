from distutils.core import setup
from setuptools import find_packages

setup(
    name = 'yz_test',
    version = '0.0',
    description = '',
    long_description = '',
    author = 'yz',
    author_email = '1084106703@qq.com',
    install_requires = [],
    packages = find_packages('src'),  # 必填，就是包的代码主目录
    package_dir = {'':'src'},
    url = "https://github.com/desion/tidy_page",
    license = '',
    classifiers = [
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Natural Language :: Chinese (Simplified)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Utilities'
    ],
    keywords = '',
    include_package_data = True,
)