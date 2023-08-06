import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rest-filter-qp",
    version="1.1.2",
    author="Mahmoud Rezaei",
    author_email="mahmoudrezaei74@gmail.com",
    description="A package for filtering any objects in django models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mahmoodrezaei/rest-filter-qp",
    project_urls={
        "Bug Tracker": "https://github.com/mahmoodrezaei/rest-filter-qp",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)