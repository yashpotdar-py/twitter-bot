from setuptools import setup, find_packages

setup(
    # Metadata about your project
    name="twitter-bot",  # The name of your project
    version="0.1.0",  # Semantic versioning
    author="Yash Potdar",
    author_email="yashyogeshpotdar7@gmail.com",
    description="A Twitter bot for automated interactions",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",

    # Project structure and packages
    packages=find_packages(where='src'),  # Important: specify source directory
    package_dir={'': 'src'},  # Tell setuptools packages are under src

    # Dependencies
    install_requires=[
        'colorama>=0.4.4',
        'requests>=2.25.1',
        # Add other dependencies from your requirements.txt
    ],

    # Optional metadata
    url="https://github.com/yashpotdar-py/twitter-bot",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],

    # Entry points if you want to create command-line scripts
    entry_points={
        'console_scripts': [
            'twitter-bot=src.main:main',  # Example of creating a CLI entry point
        ],
    },

    # Python version requirements
    python_requires='>=3.8',
)
