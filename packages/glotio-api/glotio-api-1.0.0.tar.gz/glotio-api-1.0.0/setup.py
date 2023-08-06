import setuptools

from os import path


root_dir = path.abspath(path.dirname(__file__))

with open("README.md", "r") as f:
    long_description = f.read()


def _requirements():
    return [name.rstrip() for name in open(path.join(root_dir, 'requirements.txt')).readlines()]


setuptools.setup(
    name="glotio-api",
    version="1.0.0",
    author="raster0x2a",
    author_email="raster0x2a@gmail.com",
    description="Python bindings for the glot.io API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/raster0x2a/glotio-api",
    keywords="glot.io api",
    license="MIT",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
    ],
    install_requires=_requirements(),
    python_requires=">3.4",
)
