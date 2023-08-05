import os
from setuptools import find_packages, setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='dsFramework',
    py_modules=['api_cli', 'dsFramework'],
    packages=[
        'cli',
        'cli.tester',
        'lib',
        'lib.base_classes',
        'lib.config',
        'lib.pipeline',
        'lib.shared',
        'lib.utils',
        'lib.testable',
    ],
    entry_points='''
        [console_scripts]
        ds-framework-cli=api_cli:cli
    ''',
    version='0.1.14',
    description='My first Python library',
    # url='http://pypi.python.org/pypi/PackageName/',
    author='oribrau@gmail.com',
    license='MIT',
    install_requires=required,
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
)

# commands
# for test -  python setup.py pytest
# for build wheel -  python setup-lib.py bdist_wheel
# for source dist -  python setup-lib.py sdist
# for build -  python setup-lib.py build
# for install -  python setup-lib.py install
# for uninstall - python -m pip uninstall dsframework
# for install - python -m pip install dist/dsframework-0.1.0-py3-none-any.whl

# deploy to pipy
# delete dist and build folders
# python setup-lib.py bdist_wheel
# python setup-lib.py sdist
# python setup-lib.py build
# twine upload dist/*
'''
    use
    1. python setup-lib.py install
    2. ds-framework-cli g model new_model_name
    3. twine check dist/*
    4. twine upload --repository-url https://pypi.org/legacy/ dist/*
    4. twine upload dist/*
    
    pip install dsframework --index-url https://pypi.org/simple
    
    how to use
    
    pip install dsframework
    
    ds-framework-cli generate project my-new-model
'''
