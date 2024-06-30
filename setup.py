import setuptools
import sephiroth

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sephiroth",
    version=sephiroth.__version__,
    author=sephiroth.__author__,
    author_email=sephiroth.__email__,
    maintainer=sephiroth.__maintainer__,
    description="Utility for building blocklists for ip ranges",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/0xdade/sephiroth",
    packages=["sephiroth", "sephiroth.providers"],
    install_requires=[
        "beautifulsoup4 ~= 4.11.1",
        "requests ~= 2.27.1",
        "Jinja2 ~= 3.1.1",
        "netaddr~=0.8.0",
    ],
    py_modules=["Sephiroth"],
    include_package_data=True,
    entry_points={"console_scripts": ["sephiroth = Sephiroth:main"]},
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12"
    ],
    python_requires=">=3.6",
)
