from setuptools import setup
import io
import re
from os.path import dirname
from os.path import join

def read(*names, **kwargs):
    with io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ) as fh:
        return fh.read()

setup(
    name='mmdesigner',
    description='Indoor model airplane design using OpenSCAD',
    long_description=re.compile(
        '^.. start-badges.*^.. end-badges',
        re.M | re.S
    ).sub(
        '',
        read('README.rst')
    ),
    long_description_content_type='text/x-rst',
    author='Roie R. Black',
    author_email='roie.black@gmail.com',
    url='https://github.com/rblack42/math-magik',
    license='BSD',
    version='0.1.8',
    packages=['mmdesigner'],
entry_points= {
        "console_scripts": [
            "mm = mmdesigner.__main__:main"
        ]
    },
    python_requires='>=3.7, <3.10',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Framework :: tox',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Testing',
    ],
)
