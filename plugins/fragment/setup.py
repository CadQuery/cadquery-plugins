from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

version = "1.0.0"
plugin_name = "fragment"
description = "Apply boolean fragment to solids"
long_description = "https://dev.opencascade.org/doc/overview/html/specification__boolean_operations.html#specification__boolean_7"
long_description_content_type = "text/markdown"
author = "Bruno Agostini"
author_email = "bragostin@bluewin.ch"
packages = []
py_modules = ["fragment"]
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
    long_description_content_type=long_description_content_type,
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
