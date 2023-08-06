import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py-Asteroid", # Replace with your own username
    version="0.0.0.1",
    author="ProgrammingError",
    author_email="fuck@you.com",
    description="Nothing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://notavailable.live",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)
