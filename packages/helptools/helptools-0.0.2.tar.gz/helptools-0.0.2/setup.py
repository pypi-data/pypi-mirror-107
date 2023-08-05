import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="helptools",
    version="0.0.2",
    description="The Django version of helpTools.js.",
    long_description=README,
    long_description_content_type="text/plain",
    url="",
    author="Just Leo",
    author_email="",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["helptools", "helptools.templatetags"],
    include_package_data=True,
)