import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="gattino",
    packages=setuptools.find_packages(where="./src/gattino",
                                      exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    version="0.0.1",
    license='MIT',
    author="kmuumdmrj76",
    author_email="kmuumdmrj76@163.com",
    description="gattino",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kmuumdmrj76/gattino",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    keywords=['gattino'],
    python_requires='>=3.6',
    install_requires=[
    ],
)
