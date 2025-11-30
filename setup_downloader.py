from setuptools import setup, find_packages

setup(
    name="lotto-downloader",
    version="1.0.0",
    description="Descargador de CSV con verificación VPN usando Scrapy",
    packages=find_packages(),
    install_requires=[
        "scrapy>=2.5.0",
        "requests>=2.25.0",
    ],
    entry_points={
        'console_scripts': [
            'lotto-download=lotto_downloader.cli:main',
        ],
    },
    python_requires=">=3.7",
)