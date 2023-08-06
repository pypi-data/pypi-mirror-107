#
# R. Vidmar, 20180906
# R. Vidmar, 20210103
#

from setuptools import setup, find_packages
import subprocess
import os

PACKAGE = "qcobj"
REQFILE = "requirements.txt"
EXTRAS = {
   'with_pyside2': ['PySide2>=5.14.1'],
   'with_pyqt5': ['PyQt5>=5.14.1'],
}

exec(open(os.path.join(PACKAGE, "__version__.py")).read())

with open("README.md", "r") as fh:
    long_description = fh.read()

with open(REQFILE) as fp:
    requirements = fp.read()

setup(name=PACKAGE,
        version=__version__,
        install_requires=requirements,
        author='Roberto Vidmar',
        author_email='rvidmar@inogs.it',
        description='A quantity aware configObject',
        license='MIT',
        long_description=long_description,
        long_description_content_type='text/markdown',
        url='https://bitbucket.org/bvidmar/qcobj',
        extras_require=EXTRAS,
        packages=find_packages(),
        # scripts=['bin/cfggui.py', ],
        classifiers=[
            "Programming Language :: Python :: 3.4",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.8",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            ],
        )
