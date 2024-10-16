from setuptools import setup, find_packages

setup(
    name="multi_exchange_price_aggregator",
    version="0.1.0",
    author="hedeqiang",
    author_email="laravel_code@163.com",
    description="A package for aggregating cryptocurrency prices from multiple exchanges.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/hedeqiang/multi_exchange_price_aggregator",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
