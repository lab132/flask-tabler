import os

from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    author_email='hello@lab132.com',
    author='LAB132',
    description='Flask extension for Tabler',
    include_package_data=True,
    license='MIT',
    long_description=read('README.md'),
    name='Flask-Tabler',
    packages=['flask_tabler'],
    platforms='any',
    url='http://github.com/lab132/flask-tabler',
    version='0.1.0',
    zip_safe=False,
    install_requires=[
        'Flask>=3.0',
        'visitor',
    ],
    classifiers=[
        'Environment :: Web Environment', 'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent', 'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ])