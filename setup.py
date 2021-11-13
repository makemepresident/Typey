import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="TyPy",
    version="0.0.1",
    author="makemepresident",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/makemepresident/TyPy",
    license="GNU",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    entry_points = {
        "console_scripts": ["typy = typy.typy:main"]
    },
    package_data={"typy": ["assets/*"]},
    keywords=[
        "typing",
        "typings",
        "monkeytype",
        "typingtest",
        "typey",
    ]
)