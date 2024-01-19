from setuptools import setup, find_packages

# Change these variables to set the information for your plugin
version = "1.0.0"
plugin_name = "freecad_import"  # The name of your plugin
description = "Adds FreeCAD part import support to CadQuery"
long_description = "Allows import the BRep objects from inside FCStd files, and supports altering their parameters before doing so."
author = "Jeremy Wright"
author_email = "@jmwright"
packages = []
py_modules = ["freecad_importer"]
install_requires = []


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
