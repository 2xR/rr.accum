import re

from setuptools import setup, find_packages


with open("README.md", "rt") as readme_file:
    readme = readme_file.read()

# Extract version information directly from the source code.
with open("src/rr/accum/__init__.py", "rt") as source_file:
    source = source_file.read()
match = re.search(r"__version__\s*=\s*(['\"])(\d+(\.\d+){2}([-+]?\w+)*)\1", source)
if match is None:
    raise Exception("unable to extract version from {}".format(source_file.name))
version = match.group(2)


setup(
    name="rr.accum",
    version=version,
    description="Accumulator framework with a few simple online statistics.",
    long_description=readme,
    url="https://github.com/2xR/rr.acum",
    author="Rui Jorge Rei",
    author_email="rui.jorge.rei@googlemail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Operating System :: OS Independent",
    ],
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=["future>=0.16,<0.17"],
)
