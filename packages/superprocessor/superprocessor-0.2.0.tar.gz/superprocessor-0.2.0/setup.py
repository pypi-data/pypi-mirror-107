
import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="superprocessor",
    version='0.2.0',
    author="samo",
    author_email="thesamogroup@gmail.com",
    description="SuperProcessor: the perfect wrapper for subprocess.run",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/samocorp/superprocessor",
    project_urls={
        "Bug Tracker": "https://github.com/samocorp/superprocessor/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(exclude=('tests', 'examples')),
    python_requires=">=3.6",
)