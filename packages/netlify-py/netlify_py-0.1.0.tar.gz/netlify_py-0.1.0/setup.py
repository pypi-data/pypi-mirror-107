import os
import re

from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


def get_version(*file_paths):
    """Retrieves the version from netlify_py/__init__.py"""
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = open(filename).read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


setup(
    name='netlify_py',
    version=get_version("netlify_py", "__init__.py"),
    packages=find_packages(),
    include_package_data=True,
    install_requires=["requests"],
    license='MIT License',
    description='A python wrapper for creating, managing and deploying sites to Netlify using the Netlify APIs.',
    long_description=README,
    long_description_content_type="text/markdown",
    url='https://github.com/akshay-realiq/netlify_py',
    author='akshay kumar c',
    author_email='akshay@realiq.io',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Environment :: Web Environment',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
)
