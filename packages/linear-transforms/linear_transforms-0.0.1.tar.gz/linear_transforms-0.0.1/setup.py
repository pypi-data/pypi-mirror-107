import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="linear_transforms",
    version="0.0.1",
    author="Antonio Lopez Rivera",
    author_email="antonlopezr99@gmail.com",
    description="Python coordinate frame transform library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/antonlopezr/transforms",
    packages=setuptools.find_packages(),
    install_requires=[
        "sympy",
        "numpy",
        "Python-Alexandria",
        "coverage",
        "coverage-badge"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)