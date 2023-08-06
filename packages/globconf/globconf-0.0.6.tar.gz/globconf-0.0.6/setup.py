import setuptools
import re
with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt', 'r') as f:
    requires = [re.sub(r'\s*([\w_\-\.\d]+([<>=]+\S+|)).*', r'\1', x.strip()) for x in f if
                x.strip() and re.match(r'^\s*\w+', x.strip())]


setuptools.setup(
    name="globconf",
    version="0.0.6",
    author="Steffen Schumacher",
    author_email="ssch@wheel.dk",
    description="global configparser object to be used across modules",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/steffenschumacher/globconf",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    install_requires=requires,
    setup_requires=['pytest-runner', 'wheel', 'twine'],
)
