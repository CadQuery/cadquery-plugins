from setuptools import setup, find_packages

version = "1.0.0"  # Please update this version number when updating the plugin
plugin_name = "more_selectors"
description = "Add more selectors to cadquery "
long_description = ""
author = "Romain FERRU"
author_email = "Romain.ferru@gmail.com"
install_requires = (
    []
)  # Any dependencies that pip also needs to install to make this plugin work


setup(
    name=plugin_name,
    version=version,
    url="https://github.com/CadQuery/cadquery-plugins",
    license="Apache Public License 2.0",
    author=author,
    author_email=author_email,
    description=description,
    long_description=long_description,
    packages=find_packages(where="more_selectors"),
    install_requires=install_requires,
    include_package_data=True,
    zip_safe=False,
    platforms="any",
    test_suite="tests",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX",
        "Operating System :: MacOS",
        "Operating System :: Unix",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet",
        "Topic :: Scientific/Engineering",
    ],
)
