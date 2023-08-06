import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="telegram-alpa",  # Replace with your own username
    version="0.0.1",
    author="Albert Pang",
    author_email="alpaaccount@mac.com",
    description="Python Wrapper to TelegramBot API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alpaalpa/telegram",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "requests",
        "urllib3"
    ]
)
