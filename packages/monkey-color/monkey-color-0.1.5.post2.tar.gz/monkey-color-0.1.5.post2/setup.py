from setuptools import setup
import os


this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='monkey-color',
    version='0.1.5-2',
    author='monkey',
    author_email='a102009102009@gmail.com',
    url='https://github.com/a3510377/color',
    description=u'有色文字',
    packages=['color'],
    install_requires=[],
    long_description=long_description,
    long_description_content_type='text/markdown',
)
