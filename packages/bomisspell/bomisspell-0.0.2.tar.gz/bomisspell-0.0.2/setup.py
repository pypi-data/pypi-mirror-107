import re
import setuptools
from pathlib import Path

with open("README.md", "r") as fh:
    long_description = fh.read()

def get_version(prop, project):
    project = Path(__file__).parent / project / "__init__.py"
    result = re.search(
        r'{}\s*=\s*[\'"]([^\'"]*)[\'"]'.format(prop), project.read_text()
    )
    return result.group(1)


setuptools.setup(
    name="bomisspell",  # Replace with your own username
    version=get_version("__version__", "bomisspell"),
    author="Tenzin Kaldan",
    author_email="kaldantenzin@gmail.com",
    description="Generates misspelled tibetan word of a given word",
    py_modules=["bomisspell"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="Apache2",
    url="https://github.com/potala-dev/bomisspell",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "botok>=0.8.6, <8.0",
    ],
    python_requires=">=3.8",
    tests_require=["pytest"],
)
