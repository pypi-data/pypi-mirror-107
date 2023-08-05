from setuptools import find_packages, setup

# load readme
with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="collagist",
    version="0.1.0",
    author="Chenchao Zhao",
    author_email="chenchao.zhao@gmail.com",
    description="Image collage based on PyTorch",
    packages=find_packages(exclude=["tests"]),
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["torch", "numpy"],
    license="MIT",
)

