import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="prsaw2",
    version="0.36",
    author="Flampt",
    description="Stands for Python random api wrapper version 2.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FlamptX/prsaw2",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords='python, api, rsa',
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)