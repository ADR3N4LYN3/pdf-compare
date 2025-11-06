"""
Setup script for pdf-compare
Note: This is for backwards compatibility. The project primarily uses pyproject.toml
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_file.exists():
    requirements = [
        line.strip()
        for line in requirements_file.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    ]

setup(
    name="pdf-compare",
    version="1.0.0",
    author="ADR3N4LYN3",
    description="Modern CLI tool for comparing PDF files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ADR3N4LYN3/pdf-compare",
    project_urls={
        "Bug Reports": "https://github.com/ADR3N4LYN3/pdf-compare/issues",
        "Source": "https://github.com/ADR3N4LYN3/pdf-compare",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
        ],
        "build": [
            "pyinstaller>=6.0.0",
            "cx-Freeze>=6.15.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "pdf-compare=pdf_compare.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
