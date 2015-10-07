import os

from setuptools import setup

from dayone import __version__, __project_name__, __project_link__

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = __project_name__,
    version = __version__,
    
    description = "A Python Library for the Mac OS X application Day One.",
    
    author = "Myles Braithwaite",
    author_email = "me@mylesbraithwaite.com",
    
    license = 'BSD',
    
    keywords = 'dayone',
    
    url = __project_link__,
    
    long_description = read('README.rst'),
    
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
    
    install_requires = [
        'pytz',
        'tzlocal',
        'Markdown',
    ],
    
    extras_require = {
        'cli': [ 'clint', ]
    },
    
    entry_points = {
        'console_scripts': [
            'py-dayone = dayone.cli:main [cli]'
        ]
    },
    
    test_suite = "tests"
)