import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyrnc",
    version="0.0.2",
    author="Fyodor Sizov",
    author_email="f.sizov@yandex.ru",
    description="Third-party tool to work with ruscorpora.ru",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/prodotiscus/pyrnc",
    project_urls={
        "Bug Tracker": "https://github.com/prodotiscus/pyrnc/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "pyrnc"},
    install_requires=["lxml", "flask", "requests"],
    packages=setuptools.find_packages(where="pyrnc"),
    python_requires=">=3.6",
)
