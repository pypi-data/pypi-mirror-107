import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="interlib",
    version="0.0.1",
    author="M.Kaan Karakoç",
    author_email="karakockaan326@gmail.com",
    description="A small package for intervals and timeouts similar with javascript",
    long_description=long_description,
    long_description_content_type="text/markdown",
    project_urls = {
        "Github":"https://gist.github.com/kaankarakoc42/4ff2926c6dd4dae4cdfd7b3897a3e92a"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)