from setuptools import (find_packages, setup)

with open('README.md', 'r') as readme:
    long_description = readme.read()

setup(
    author='amancevice',
    author_email='smallweirdnum@gmail.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Framework :: AsyncIO',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Utilities',
    ],
    description='Simple and visually consistent logger for AWS Lambda',
    install_requires=[],
    long_description=long_description,
    long_description_content_type='text/markdown',
    name='lambo',
    packages=find_packages(exclude=['tests']),
    python_requires='>= 3.7',
    setup_requires=['setuptools_scm'],
    url='https://github.com/amancevice/python-lambo',
    use_scm_version=True,
)
