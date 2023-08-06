import setuptools

with open("README.md", "r", encoding='utf-8') as f:
    _description = f.read()

setuptools.setup(
    name="pilmoji",
    version="1.3.2",
    author="jay3332",
    description="Pilmoji is a fast and reliable emoji renderer for PIL.",
    long_description=_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jay3332/pilmoji",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)
