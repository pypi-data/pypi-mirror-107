import codecs
import setuptools


setuptools.setup(
    name="vinca",
    version="1.1.39",
    author="Oscar Laird", # your name
    author_email="olaird25@gmail.com", # your email
    description="A simple spaced repetition system",
    long_description=codecs.open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    license="MIT", # license type
    include_package_data = True,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5', # python version
    install_requires=[ # dependecies package
        'readchar',
    ],
    entry_points = {
        'console_scripts': ['vinca=vinca.run:main']
    },
)
