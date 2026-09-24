from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="stealthkit",
    version="1.1.1",
    author="Anil Sardiwal",
    author_email="theonlyanil@gmail.com",
    license_files=('LICENSE',),
    description="A stealthy HTTP request library with rotating user agents and proxy support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/theonlyanil/stealthkit",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "curl-cffi==0.10.0",
        "fake-useragent==2.0.3"
    ],
    extras_require={
        "solver": ["playwright>=1.40.0"]
    }
) 