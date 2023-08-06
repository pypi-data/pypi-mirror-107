import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="amxmaintenance",
    version="0.0.4",
    author="Logan Vaughn",
    # author_email="logantv@gmail.com",
    description="amx telnet info, firmware checks, logs, etc.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/logantv/amxmaintenance",
    project_urls={
        "Bug Tracker": "https://github.com/logantv/amxmaintenance/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
		'amxtelnet',
		'amxlogs',
		'exceltoamx',
		'amxtoexcel',
        'amxfirmware',
	],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)