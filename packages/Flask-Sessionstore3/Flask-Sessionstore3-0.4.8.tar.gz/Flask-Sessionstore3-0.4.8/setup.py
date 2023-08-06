"""
Flask-Session
-------------

Flask-Session is an extension for Flask that adds support for 
Server-side Session to your application.

"""
from setuptools import setup
from setuptools import find_packages

setup(
    name='Flask-Sessionstore3',
    version='0.4.8',
    url='https://github.com/fgiamma/flask-sessionstore3',
    license='BSD',
    author='Fabrizio Giammatteo',
    author_email='fabrizio.giammatteo@gmail.com',
    description='Adds session support to your Flask application, upgraded to Flask 2.0',
    long_description=__doc__,
    packages=['flask_sessionstore'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask>=0.8',
        'cachelib>=0.1.1'
    ],
    #package_dir={"": "flask_sessionstore"},
    #packages=find_packages(where="flask_sessionstore"),
    test_suite='test_session',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
