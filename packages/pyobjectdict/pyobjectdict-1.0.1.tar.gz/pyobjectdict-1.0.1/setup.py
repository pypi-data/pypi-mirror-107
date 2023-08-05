from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'pypireadme.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name = 'pyobjectdict',
    packages = ['pyobjectdict'],
    version = '1.0.1',
    license='MIT',
    description = 'Package provides a js-like dictionary object with a more convenient support of dot syntax plus a few additional methods',
    long_description_content_type='text/markdown',
    long_description=long_description,
    author = 'Serhii Orkivskyi',
    author_email = '2blesteve@gmail.com',
    url = 'https://github.com/keptt/pyobjectdict',
    download_url = 'https://github.com/keptt/pyobjectdict/archive/refs/tags/1.0.1.tar.gz',
    keywords = ['dict', 'objectdict', 'pyobjectdict', 'dot syntax', 'object', 'pyobject', 'js-like', 'js'],
    install_requires=[],
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 3 - Alpha',      # "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of the package
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
