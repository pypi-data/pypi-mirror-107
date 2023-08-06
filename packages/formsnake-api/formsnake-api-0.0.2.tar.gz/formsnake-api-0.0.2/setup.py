import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()
init_contents = (HERE / "formsnake" / "__init__.py").read_text()
version = "0.0.2"

setup(
    name="formsnake-api",
    version=version,
    description="Open Source alternative to Google Forms.",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Dakota Brown",
    author_email="dakota.kae.brown@gmail.com",
    url="https://github.com/formsnake/formsnake-api",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
    ],
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=[
        "flask>=2",
        "flask-sqlalchemy",
        "flask-marshmallow",
        "flask-mail",
        "marshmallow-sqlalchemy",
        "psycopg2",
        "cx_oracle",
        "pymssql",
        "pycryptodome",
        "alembic",
        "pymysql",
        "python-dotenv",
        "flask-bcrypt",
        "flask-mail",
        "beautifulsoup4",
        "uwsgi",
        "flask-cors",
        "PyJWT",
    ],
)
