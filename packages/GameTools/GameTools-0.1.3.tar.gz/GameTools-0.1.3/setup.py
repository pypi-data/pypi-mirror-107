import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="GameTools",
    version="0.1.3",
    author="Spidertyler2005",
    author_email="spidertyler1122@gmail.com",
    description="A bunch of tools for making games in Pygame and other libraries.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/spidertyler2005/GameTools",
    project_urls={
        "Bug Tracker": "https://github.com/spidertyler2005/GameTools/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src/"},
    packages=["GameTools","GameTools.Entity","GameTools.Templates","GameTools.Timing","GameTools.Tools","GameTools.Tools.Math"],
    install_requires=["pygame"],
    python_requires=">=3.8",
)