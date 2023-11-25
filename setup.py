from distutils.core import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="reddit-python-api",
    packages=["redditpythonapi"],
    version="0.8",
    license="GPLv3",
    description="A simple Reddit Python API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Electronic Mango",
    author_email="78230210+Electronic-Mango@users.noreply.github.com",
    url="https://github.com/Electronic-Mango/reddit-python-api",
    download_url="https://github.com/Electronic-Mango/reddit-python-api/releases/",
    project_urls={
        'Documentation': 'https://electronic-mango.github.io/reddit-python-api',
        'Source': 'https://github.com/Electronic-Mango/reddit-python-api',
    },
    keywords=["reddit", "api"],
    install_requires=["httpx"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
