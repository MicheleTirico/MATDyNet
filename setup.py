from setuptools import find_packages, setup
setup(
    name='matdynet',
    packages=find_packages(
        include=['matdynet']),
    version='0.2.0',
    description='project',
    author='Me',
    license='MIT',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='test',
)
