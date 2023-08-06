import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="auto-aiml",
    version="1.0.4",
    description="Creates a best predictive regression/classification model ",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/yashu7890/yash",
    author="Yashwanth Agastya",
    author_email="admin@yash.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["aiml"],
    include_package_data=True,
    install_requires=[
        "numpy","pandas","scipy",'sklearn',"imblearn","xgboost"
    ],
    entry_points={
        "console_scripts": [
            "aiml=aiml.__main__:main",
        ]
    },
)
