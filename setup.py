#!/usr/bin/env python3
"""
Setup configuration for Bibliography Generator
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="bibliography-generator",
    version="1.0.0",
    description="High-performance bibliography generator with ML field extraction",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/bibliography-generator",
    packages=find_packages(exclude=["tests", "docs", "output"]),
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering",
        "Topic :: Text Processing",
    ],
    keywords="bibliography citations bibtex ieee apa chicago mla",
    entry_points={
        "console_scripts": [
            "bibliography=src.enhanced_main:main",
        ],
    },
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "black>=22.0",
            "flake8>=4.0",
            "mypy>=0.990",
        ],
    },
)
