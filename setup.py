import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="unicaps",
    version="1.2.0",
    author="Sergey Scat",
    author_email="py.unicaps@gmail.com",
    description="Universal CAPTCHA Solver for humans",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sergey-scat/unicaps",
    packages=setuptools.find_packages(),
    install_requires=["httpx>=0.22.0", "enforce-typing>=1.0.0"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10"
    ],
    python_requires='>=3.7',
)
