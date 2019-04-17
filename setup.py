from setuptools import setup, find_packages

setup(
    name='diskmond',
    version='0.1',
    py_modules=['diskmond'],
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    package_data={'diskmond': ['*']},
    install_requires=[
        'Click==7.0',
        'pysmart.smartx==0.3.9',
    ],
    extras_require={
        'statsd':  ['statsd==3.3.0'],
        'datadog': ['datadog==0.28.0'],
    },
    entry_points='''
        [console_scripts]
        diskmond=diskmond.main:cli
    ''',
)
