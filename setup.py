from setuptools import setup, find_packages

setup(
    name='diskmond',
    version='0.1',
    py_modules=['diskmond'],
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    install_requires=[
        'Click==7.0',
        'pysmart.smartx==0.3.9',
        'statsd==3.3.0'
    ],
    entry_points='''
        [console_scripts]
        diskmond=diskmond.main:cli
    ''',
)
