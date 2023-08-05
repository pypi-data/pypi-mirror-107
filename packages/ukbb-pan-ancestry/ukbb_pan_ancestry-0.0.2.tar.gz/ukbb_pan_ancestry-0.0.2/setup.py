import setuptools


with open("README.md", "r", encoding="utf-8") as readme_file:
    long_description = readme_file.read()

requirements = []
with open("requirements.txt", "r") as requirements_file:
    for req in (line.strip() for line in requirements_file):
        requirements.append(req)

setuptools.setup(
    name="ukbb_pan_ancestry",
    version="0.0.2",
    author="",
    author_email="",
    description="Functions for GWAS across all analyzable phenotypes and diverse ancestry groups in the UK Biobank.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/atgu/ukbb_pan_ancestry",
    project_urls={
        "Source Code": "https://github.com/atgu/ukbb_pan_ancestry",
        "Issues": "https://github.com/atgu/ukbb_pan_ancestry/issues",
    },
    classifiers=[
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
    ],
    python_requires=">=3.6",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=requirements,
)
