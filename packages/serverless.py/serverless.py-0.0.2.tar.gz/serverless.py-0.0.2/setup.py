import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name="serverless.py",
    version="0.0.2",
    author="Matheus Vinícius",
    author_email="mtwzim@gmail.com",
    description="A Simple Decorator to create a REST Python API in serverless",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mtwzim/python-serverless",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_required=">=3.7.9"
);
