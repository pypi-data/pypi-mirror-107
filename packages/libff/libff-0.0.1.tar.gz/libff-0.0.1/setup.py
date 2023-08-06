import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="libff",
    version="0.0.1",
    author="ilia85-star",
    author_email="ilia.mahjour.shafiei@outlook.com",
    description="a factor calculator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ilia85-star/libff",
    project_urls={
        "Bug Tracker": "https://github.com/ilia85-star/libff/issues",
    },
    entry_points={
        "console_scripts": ["libff = libff.libff:main"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
