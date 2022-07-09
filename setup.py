from setuptools import setup, find_packages

long_description = open('README.md').read()


setup(
    name='redis-pydict',
    version='0.0.1',
    author='Narasimha Prasanna HN',
    author_email='narasimhaprasannahn@gmail.com',
    url='https://github.com/Narasimha1997/redis-pydict',
    description="A python dictionary that uses Redis as in-memory storage backend to facilitate distributed computing applications development.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    packages=find_packages(),
    classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
    ],
    keywords='python redis distributed-computing dict software-dev',
    zip_safe=False,
    install_requires=[
        "redis"
    ]
)