# -*- coding: UTF-8 -*-
from setuptools import setup

with open("README.md", "r", encoding='utf8') as fp:
    long_description = fp.read()

setup(
    name='Flask-MySQLPooled',
    version='0.1.1',
    url='https://github.com/wanganhong/flask-mysqlpooled/',
    license='BSD',
    author='wanganhong',
    author_email='773624972@qq.com',
    description='A Flask mysql pool extension based on DBUtils',
    long_description=long_description,
    long_description_content_type='text/markdown',
    py_modules=['flask_mysqlpooled'],
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask',
        'PyMySQL',
        'DBUtils'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
