import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="djangmx",
    version="0.0.6",
    author="Logan Vaughn",
    # author_email="logantv@gmail.com",
    description="handles communication between AMX masters and django",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/logantv/djangmx",
    project_urls={
        "Bug Tracker": "https://github.com/logantv/djangmx/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # install_requires=[
    #     "ftplib == *",
    # ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
