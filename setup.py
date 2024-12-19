from setuptools import setup, find_packages

setup(
    name="twitter-bot",
    version="0.1.0",
    author="Yash Potdar",
    author_email="yashyogeshpotdar7@gmail.com",
    description="A Twitter bot for automated interactions",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",

    packages=find_packages(where='src'),
    package_dir={'': 'src'},

    install_requires=[
        "selenium"
        "requests"
        "requests_oauthlib"
        "python-dotenv"
        "webdriver-manager"
        "google-generativeai"
        "scikit-learn"
    ],

    url="https://github.com/yashpotdar-py/twitter-bot",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],

    entry_points={
        'console_scripts': [
            'twitter-bot=src.main:main',
        ],
    },

    python_requires='>=3.8',
)
