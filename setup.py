import os
from setuptools import setup

setup(
    name = "plocal",
    version = "0.1",
    author = "Dave Mankoff",
    author_email = "mankyd@gmail.com",
    description = ("A \"local\" storage class that mirrors threading.local but works across multiple processes as well as threads."),
    license = "BSD",
    keywords = "fork multiprocessing threading local storage",
    url = "http://ohthehugemanatee.net/",
    packages=['plocal'],
    test_suite='tests',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Software Development",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
