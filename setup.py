from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="public_tunnel",
    version="0.1.0",
    author="Public Tunnel Team",
    description="A network tunneling solution for AI assistants to control devices in non-directly accessible network environments",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=[
        "fastapi[standard]==0.116.1",
        "uvicorn==0.35.0",
        "pydantic==2.9.2",
        "python-multipart",
        "aiofiles",
    ],
    extras_require={
        "test": [
            "pytest==8.4.1",
            "pytest-asyncio==1.1.0",
            "pytest-bdd==8.1.0",
            "pytest-env==1.1.5",
            "httpx==0.28.1",
        ],
        "dev": [
            "pytest==8.4.1",
            "pytest-asyncio==1.1.0",
            "pytest-bdd==8.1.0",
            "pytest-env==1.1.5",
            "httpx==0.28.1",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Tools",
        "Topic :: System :: Distributed Computing",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
    ],
)