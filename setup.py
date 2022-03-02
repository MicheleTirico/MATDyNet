from setuptools import find_packages, setup
setup(
    name='matdynet',
    packages=find_packages(include=['matdynet']),		# NAME project here
    version='0.1.0',
    description='project',
    author='Me',
    license='MIT',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)
