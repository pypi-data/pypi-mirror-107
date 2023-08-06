from setuptools import setup

setup(
    name='tw-stocks',
    author='PJ',
    author_email='pjwang0710@gmail.com',
    description="tw stocks infos",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url='https://github.com/pjwang0710/tw-stocks',
    version='0.1.0',
    license='MIT',
    packages=['tw_stocks'],
    install_requires=[
        'requests>=2.0.0',
    ],
    tests_require=[
        'pytest',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Testing',
    ]
)