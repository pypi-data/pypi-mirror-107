from setuptools import setup, find_packages
import os


VERSION = '0.0.2'
DESCRIPTION = 'Coverting an excel sheet of contacts to Google contacts suppoerted csv format'
LONG_DESCRIPTION = 'A simple library for coverting an excel sheet of contacts to Google contacts suppoerted csv format. Note that the package requires Pandas framework'

# Setting up
setup(
    name="contacts2csv",
    version=VERSION,
    author="Nerlin Maria Thomas and Mebin Joy",
    author_email="<nerlinandmebin@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pandas'],
    keywords=['python', 'contacts','google_contacts'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)