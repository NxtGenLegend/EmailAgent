from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="email-agent",
    version="1.0.0",
    author="Adhish Chakravorty",
    author_email="skjetly094@gmail.com",
    description="Simple Gmail inbox monitor with periodic email summaries",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NxtGenLegend/EmailAgent",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        "google-auth>=2.23.0",
        "google-auth-oauthlib>=1.1.0",
        "google-auth-httplib2>=0.1.0",
        "google-api-python-client>=2.100.0",
    ],
    entry_points={
        "console_scripts": [
            "EmailAgent=EmailAgent.agent:main",
        ],
    },
    include_package_data=True,
    package_data={
        "EmailAgent": ["*.py"],
    },
)