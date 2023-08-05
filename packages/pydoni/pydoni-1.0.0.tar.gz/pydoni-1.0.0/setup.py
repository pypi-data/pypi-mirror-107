#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

# with open('requirements.in') as requirements_file:
#     requirements = requirements_file.read().split()

requirements = [
    'SQLAlchemy==1.4.7',
    'psycopg2-binary==2.8.6',
    'click==8.0.0',
    'colr==0.9.1',
    'matplotlib==3.4.2',
    'pylab-sdk==1.3.2',
    'PyInquirer==1.0.3',
    'requests==2.25.1',
    'pytest==6.2.4',
    'colorlog==5.0.1',
    'pandas==1.2.4',
    'emoji==1.2.0',
    'tqdm==4.60.0',
    'PyExifTool==0.4.7',
    'colr==0.9.1',
    'beautifulsoup4==4.9.3',
    'mutagen==1.45.1',
    'scenedetect==0.5.5',
    'opencv-python==4.5.2.52',
    'lxml==4.6.3',
    'pytesseract==0.3.7',
    'pydub==0.25.1',
    'google-cloud-speech==2.3.0',
]

setup(
    author='Andoni Sooklaris',
    author_email='andoni.sooklaris@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    description='A Python module for custom-built tools and maintained by Andoni Sooklaris.',
    entry_points={
        'console_scripts': [
            'pydoni=pydoni.cli:main',
        ],
    },
    install_requires=requirements,
    license='MIT license',
    # long_description=readme + '\n\n' + history,
    # include_package_data=True,
    keywords='pydoni',
    name='pydoni',
    packages=find_packages(include=['pydoni', 'pydoni.*'], exclude=['tests*']),
    setup_requires=[],
    # test_suite='tests',
    # tests_require=['pytest==6.2.4'],
    url='https://github.com/tsouchlarakis/pydoni',
    version='1.0.0',
    zip_safe=False,
)
