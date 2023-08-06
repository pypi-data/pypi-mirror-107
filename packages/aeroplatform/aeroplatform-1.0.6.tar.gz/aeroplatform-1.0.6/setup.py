import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aeroplatform",
    version="1.0.6",
    author="Aero Technologies",
    author_email="aero@robbiea.co.uk",
    description="A simple Data Infrastructure Platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    install_requires=[
        'click>=7.0',
        'requests',
        'boto3',
        'pylint<2.5.0',
        'aero-metaflow'
    ],
    entry_points={
        'console_scripts': [
            'aero = aeroplatform.cli:cli',
        ],
    }
)