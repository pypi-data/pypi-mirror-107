import setuptools

#https://stackoverflow.com/questions/1471994/what-is-setup-py#:~:text=setup.py%20is%20a%20python,to%20easily%20install%20Python%20packages.
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="googlewrapper",
    version="0.1.0",
    author="Jace Iverson",
    author_email="iverson.jace@gmail.com",
    description="simple wrapper on Google API connections",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jaceiverson/google-wrapper",
    packages = ["googlewrapper"
            ]

)
