from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='test-zzz-sdk',
    version='2.1.3',
    description='xxx CRM SDK for xxx CRM 2.1 APIs',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/xxx/xxxcrm-python-sdk',
    author='xxx CRM API Team',
    author_email='support@xxxcrm.com',
    scripts=[],
    classifiers=[
        'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.7',
    ],
    install_requires=[
        'requests',
        'python-dateutil',
        'urllib3'
    ],

    # What does your project relate to?
    keywords=['development', 'xxx', 'crm', 'api', 'zcrmsdk', 'sdk', 'zcrm'],

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(),
    include_package_data=True
)