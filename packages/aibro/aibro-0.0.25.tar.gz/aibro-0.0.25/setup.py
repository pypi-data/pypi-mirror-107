from setuptools import find_packages
from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="aibro",
    version="0.0.25",
    author="AIpaca.ai",
    author_email="codyw@aipaca.ai",
    description="Seamingless model training",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ziyincody/AIbro_cli",
    project_urls={
        "Bug Tracker": "https://github.com/ziyincody/AIbro_cli/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    install_requires=["python-socketio"],
    python_requires=">=3.6",
)
