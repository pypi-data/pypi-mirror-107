import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setuptools.setup(
    name="classesqgs",
    version="0.0.2",
    author="quantumgames studios",
    author_email="ttvquantumgames27@gmail.com",
    description="A small example package",
    long_description="idk",
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "class"},
    packages=setuptools.find_packages(where="class"),
    python_requires=">=3.6",
)
