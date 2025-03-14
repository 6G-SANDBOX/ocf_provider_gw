from setuptools import setup, find_packages

setup(
    name="provider_gw",
    version="0.1",
    author="JorgeEcheva",
    url="https://github.com/Telefonica/pesp_provider_gw",
    author_email="jorge.echevarriauribarri.practicas@telefonica.com",
    description="PROVIDER_GW is a component designed to facilitate the integration of legacy systems with the Common API Framework (CAPIF).",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(), 
    python_requires=">=3.9",
    install_requires=[
        "annotated-types==0.7.0",
        "anyio==4.6.2.post1",
        "arrow==1.3.0",
        "binaryornot==0.4.4",
        "blinker==1.9.0",
        "certifi==2024.7.4",
        "cffi==1.17.1",
        "chardet==5.2.0",
        "charset-normalizer==3.4.0",
        "click==8.1.7",
        "coverage==4.5.4",
        "cryptography==38.0.4",
        "ecdsa==0.19.0",
        "fastapi==0.115.5",
        "flake8==3.9.2",
        "Flask==3.0.3",
        "Flask-JWT-Extended==4.6.0",
        "h11==0.14.0",
        "idna==3.7",
        "iniconfig==2.0.0",
        "itsdangerous==2.2.0",
        "Jinja2==3.1.4",
        "jinja2-time==0.2.0",
        "MarkupSafe==2.1.5",
        "mccabe==0.6.1",
        "opencapif_sdk==0.1.20",
        "packaging==24.2",
        "pip==24.0",
        "pluggy==1.5.0",
        "pyasn1==0.6.1",
        "pycodestyle==2.7.0",
        "pycparser==2.22",
        "pydantic==2.10.0",
        "pydantic_core==2.27.0",
        "pyflakes==2.3.1",
        "PyJWT==2.10.0",
        "pyOpenSSL==22.1.0",
        "pytest==8.3.2",
        "python-dateutil==2.9.0.post0",
        "python-jose==3.3.0",
        "PyYAML==6.0.1",
        "requests==2.32.3",
        "rsa==4.9",
        "six==1.16.0",
        "sniffio==1.3.1",
        "starlette==0.41.3",
        "text-unidecode==1.3",
        "types-python-dateutil==2.9.0.20241003",
        "urllib3==2.2.2",
        "uvicorn==0.32.1",
        "Werkzeug==3.0.4",
    ],
    entry_points={
        "console_scripts": [
            "provider_gw=provider_gw.cli:main"  
        ],
    },
)
