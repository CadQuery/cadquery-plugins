from setuptools import setup, find_packages

# Change these variables to set the information for your plugin
version = "1.0.0"  # Please update this version number when updating the plugin
plugin_name = "heatserts"  # The name of your plugin
description = "Holes to suit heatserts"
long_description = "Save time by creating standard holes for commonly used heatserts. Heatserts are often used for 3D printed parts."
author = "Marcus Boyd"
author_email = "marcus7070@github"
packages = []  # List of packages that will be installed with this plugin
py_modules = ["heatserts"]  # Put the name of your plugin's .py file here
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
