from setuptools import setup, find_packages

version = "1.0.0"
plugin_name = "apply_to_each_face"  # The name of your plugin
description = "Building the same geometry on each selected face"
long_description = (
    "This plugin "
    + "simplifies using each(..) on faces. To use each "
    + "you have to select workplane coordinate system for each"
    + "face before building your geometry. "
    + "applyToEachFace() function provided by this plugin "
    + "separates tasks of choosing face coordinate system and "
    + "actually building new geometry and provides a few built in "
    + "ways of choosing coordinate system that are good enough in "
    + "many cases."
)
author = "Fedor Kotov"
author_email = "fedorkotov@gmail.com"
packages = []  # List of packages that will be installed with this plugin
py_modules = ["apply_to_each_face"]  # Put the name of your plugin's .py file here
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
    packages=packages,
    py_modules=py_modules,
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
