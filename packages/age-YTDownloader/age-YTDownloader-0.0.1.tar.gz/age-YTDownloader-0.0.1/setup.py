from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'YT video stream downloader'
LONG_DESCRIPTION = 'Package for aquiring binary data for YouTube videos with age restrictions.'

# Setting up
setup(
    name="age-YTDownloader",
    version=VERSION,
    author="Moonbox88 (Sean Mooney)",
    author_email="<seanmooney@live.co.uk>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['pytube', 'ffmpy'],
    keywords=['python', 'video', 'stream', 'YouTube'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
