import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kkbox_interview_orgchart",
    version="0.0.1",
    author="Eric Chen",
    author_email="eric19920108@gmail.com",
    description="A KKBOX interview demo",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/Ericchen0108/kkbox",
    project_urls={
        "Bug Tracker": "https://gitlab.com/Ericchen0108/kkbox",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
)