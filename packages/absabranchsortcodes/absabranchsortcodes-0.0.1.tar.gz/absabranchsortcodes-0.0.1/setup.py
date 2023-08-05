import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()
with open("requirements.txt", "r") as fh:
    requirements = [line.strip() for line in fh]

setuptools.setup(
    name="absabranchsortcodes",
    version="0.0.1",
    author="Hendrik du Toit",
    author_email="hendrik@brightedge.co.za",
    description="ABSA Branch Sort Codes Generator.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    # package_dir={"": "src"},
    # packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=requirements,
)
