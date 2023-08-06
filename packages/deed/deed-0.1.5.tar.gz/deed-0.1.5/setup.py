import os
import subprocess

from setuptools import find_packages, setup


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname), encoding='utf-8').read()


def version():
    git_version = None
    try:
        git_tag = subprocess.check_output(['git', 'describe', '--tags'])
        if git_tag:
            git_version = git_tag.strip()[1:].decode('utf-8')
    except:
        pass
    if not git_version:
        git_version = 'SNAPSHOT'
    return git_version


setup(
    name='deed',
    version=version(),
    description='ActivityFormatter for object changes (auditlog)',
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    author='TruckPad',
    url='https://github.com/TruckPad/deed-py',
    scripts=[],
    packages=find_packages(exclude=['tests*']),
    install_requires=['jsonpatch>=1.32'],
    extra_requires={"bottle": ['bottle~=0.12']},
    license="Apache License 2.0",
    python_requires=">= 2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*",
)
