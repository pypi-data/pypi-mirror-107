from setuptools import find_packages, setup

setup(
    name = 'halohalo',
    packages = find_packages(include = ['halohalo']),
    version = '0.0.7',
    description = 'Randomized AB Testing Library used for integrating with ML Deployments',
    author = 'Miles Ong',
    license = 'MIT',
    install_requires = []
    # setup_requires = ['pytest-runner'],
    # tests_require = ['pytest==4.4.1'],
    # test_suite = 'tests'
)