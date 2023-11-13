from distutils.core import setup

setup(
    name="reddit-python-api",
    packages=["redditpythonapi"],
    version="0.2",
    license="GPLv3",
    description="A simple Reddit Python API",
    author="Electronic Mango",
    author_email="78230210+Electronic-Mango@users.noreply.github.com",
    url="https://github.com/Electronic-Mango/reddit-python-api",
    download_url="https://github.com/Electronic-Mango/reddit-python-api/releases/tag/0.2",
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
