from setuptools import setup, find_packages


DESCRIPTION = "An async wrapper for the Tenor and Giphy API's"

# Setting up
setup(
    name="aiogifs",
    version="0.0.7",
    author="moonie",
    author_email="wishymovies@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=open("README.md").read(),
    packages=find_packages(),
    install_requires=["aiohttp"],
    keywords=[
        "aiohttp", "gif", "gifs", "tenor", "api", "giphy"
    ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    project_urls={"GitHub": "https://github.com/muunie/aiogifs"},
)