from setuptools import setup, find_packages

setup(
    name="pixel-invaders",
    version="1.0.0",
    packages=find_packages(),
    install_requires=["pyxel"],
    entry_points={"console_scripts": ["pixel-invaders = pixel_invaders.main:Main"]},
    include_package_data=True,
    package_data={
        "pixel_invaders": ["data/*.json", "assets/images/*.png"]
    },
    author="Léo Leman",
    description="A fun little retro pixel art game where you defend the galaxy against an alien invasion.",
    long_description=open("docs/README_PYPI.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/LeoLeman555/Pixel_Invaders",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
)
