import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Typey",
    version="1.0.4",
    author="makemepresident",
    description="A terminal typing test based on the likes of \
        monkeytype.gg and typings.gg, visualized with the blessed library.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/makemepresident/Typey",
    license="GNU",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Games/Entertainment",
        "Operating System :: Microsoft :: Windows",
        "Natural Language :: English",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Intended Audience :: End Users/Desktop",
        "Environment :: Console :: Curses"
    ],
    entry_points = {
        "console_scripts": ["typey = typey.typey:main"]
    },
    package_data={"typey": ["assets/*"]},
    keywords=[
        "10fastfingers",
        "typeracer",
        "typing test",
        "typey",
        "typing",
        "typings",
        "monkeytype",
        "typingtest",
        "type",
        "keyboard",
        "terminal",
        "blessed",
        "curses",
        "mechanical keyboard"
    ]
)