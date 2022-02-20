from setuptools import setup

__version__ = "1.0.0"

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='yctl',
    version=__version__,
    description='Query and control an Yggdrasil Network node with Admin API',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['yctl'],
    url='https://github.com/zhoreeq/yctl',
    author='zhoreeq',
    author_email='zhoreeq@protonmail.com',
    license='LGPL',
    keywords='yggdrasil network mesh',
    python_requires='>=3',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Communications',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Programming Language :: Python :: 3',
    ],
)
