from distutils.core import setup

# Change these variables to set the information for your plugin
version = '0.0.1' # Please update this version number when updating the plugin
plugin_name = 'more_selectors' # The name of your plugin
description = 'Add more selectors to cadquery '
long_description = ''
author = 'Romain FERRU'
author_email = 'Romain.ferru@gmail.com'
packages = [] # List of packages that will be installed with this plugin
py_modules = ["more_selectors", "utils"] # Put the name of your plugin's .py file here
install_requires = [] # Any dependencies that pip also needs to install to make this plugin work


setup(
    name=plugin_name,
    version=version,
    url='https://github.com/CadQuery/cadquery-plugins',
    license='Apache Public License 2.0',
    author=author,
    author_email=author_email,
    description=description,
    long_description=long_description,
    packages=packages,
    py_modules=py_modules,
    install_requires=install_requires,
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    test_suite='tests',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet',
        'Topic :: Scientific/Engineering'
    ]
)