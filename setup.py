from setuptools import setup, find_packages

setup(
    name="db-toolkit",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.103.0",
        "uvicorn==0.23.2",
        "sqlparse==0.4.4",
        "psycopg2==2.9.9",
        "python-dotenv==1.0.0",
        "sentence-transformers==2.2.2",
    ],
    entry_points={"console_scripts": ["db-toolkit = backend.cli:main"]},
    author="Pranav",
    description="AI-powered SQL optimizer and vector playground",
    url="https://github.com/pranavkp71/IQuerio",
)
