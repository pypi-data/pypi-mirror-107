"""
To build distribution: python setup.py sdist bdist_wheel
"""

import os
import setuptools

pkg_name = 'pytgen'
version = '0.0.2'

# read long description from readme.md
base_dir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(base_dir, 'readme.md')) as fd:
    long_description = fd.read()

setuptools.setup(
    name=pkg_name,
    version=version,
    description='A simple traffic generator',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ashutshkumr/pytgen',
    author='Ashutosh Kumar',
    author_email='ashutshkumr@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing :: Traffic Generation',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
    keywords='pytgen',
    packages=[pkg_name],
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=[],
)
