from setuptools import setup, find_packages

setup(
    name="hypertgdownloader",  # Must be unique on PyPI
    version="0.1.0",  # Start with 0.1.0
    description="High-speed Telegram downloader using multiple helper bots",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",  # Replace with your name
    author_email="your.email@example.com",  # Replace with your email
    url="https://github.com/tanmayf/hypertgdownloader",  # Replace with your GitHub repo (optional)
    packages=find_packages(),
    install_requires=[
        "pyrogram>=2.0.0",
        "aiofiles",
        "aioshutil",
    ],
    python_requires=">=3.8",
    include_package_data=True,
    package_data={
        "hypertgdownloader": ["examples/*.py"],
    },
)
