import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pgb",
    version="0.0.1",
    author="ilia85-star",
    author_email="ilia.mahjour.shafiei@outlook.com",
    description="Create a progress bar",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ilia85-star/pgb",
    project_urls={
        "Bug Tracker": "https://github.com/ilia85-star/pgb/issues",
    },
    entry_points={
        "console_scripts": ["pgb = pgb.pgb:main"],
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
