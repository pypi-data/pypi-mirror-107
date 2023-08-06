from setuptools import setup, find_packages

with open("README.md") as f:
    long_description = f.read()

setup(
    name="localhook",
    version="0.0.3",
    url="https://github.com/kekayan/localhook",
    author="Kekayan Nanthakumar",
    author_email="kekayan.nanthakumar@gmail.com",
    description="Receive webhooks to your Terminal",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    py_modules=["localhook"],
    install_requires=[
        "pyngrok>=5.0.2",
        "Flask==2.0.1",
        "PyYAML>=5.3.1",
        "rich",
        "waitress",
        "click==8.0.1",
    ],
    entry_points="""
            [console_scripts]
            localhook=localhook:start
    """,
)
