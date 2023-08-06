from distutils.core import setup


setup(
    name="ioeeoap",
    packages = ['mypackage'],
    scripts = [],
    version="0.5.0",
    author="Yu Zhen、Guan Wei、Zhilin",
    author_email="",
    description="It is a specific form of the content of the economic effect of agricultural production through numerical values. ",
    license="MIT",
    url="",
    include_package_data=True,
    keywords = ['pypi'],
    classifiers=[
        "Environment :: Web Environment",
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: Microsoft',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    install_requires=[
            'pandas>=0.20.0',
            'numpy>=1.14.0'
            ],
    )