from setuptools import setup, find_packages

with open("README.md", "r", encoding ="utf8") as f:
    long_description = f.read()

setup(
    name="autolist",
    version="0.0.4",
    author="Abel Roy",
    author_email="abelroi007@gmail.com",
    description="Auto-Corrects mistyped words by checking them with the list of given correct words",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AbelR007/Autolist",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
