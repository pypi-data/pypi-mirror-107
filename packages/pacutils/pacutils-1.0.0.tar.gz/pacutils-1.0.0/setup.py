import setuptools


setuptools.setup(
    name="pacutils",
    version="1.0.0",
    author="Wei Huang",
    author_email="wei.huang@intel.com",
    description="PAC utilities",
    long_description="file: README.md",
    long_description_content_type="text/markdown",
    url="https://gitlab.devtools.intel.com/OPAE/pyopae",
    platforms="Linux",
    license="BSD3",
    keywords="PAC OPAE",
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'pac_op = pacutils.pac_op:main'
        ]
    },
    classifiers=["Programming Language :: Python :: 3",
                 "License :: OSI Approved :: BSD License",
                 "Operating System :: POSIX :: Linux",
                ],
    install_requires=['pyopae'],
    python_requires='>=3.6',
)
