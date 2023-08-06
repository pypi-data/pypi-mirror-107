# Import Required Libraries
import os
from codecs import open
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__),"README.md")) as f:
    long_description = f.read()

# Setup Parameters
setup(
    name = 'test-module-vicky',
    packages = ['test-module-vicky'],
    version = '1.0.0',
    license = 'MIT License',
    description = 'Sample Description string',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    author = 'Vigneshwar K R',
    author_email = 'vicky.pcbasic@gmail.com',
    url = 'https://github.com/ToastCoder/test-module-vicky',
    download_url = 'https://github.com/ToastCoder/test-module-vicky/archive/master.zip',
    keywords = ['LEARNING'],
    install_requires = ['numpy'],
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Education',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3',
    ]
)