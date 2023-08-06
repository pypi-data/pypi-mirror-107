from setuptools import setup

setup(
    name='si_cli',
    version='0.0.1',
    packages=['si_cli'],
    author="Lukas Jurk",
    author_email="ljurk@pm.me",
    description="convert resistor and capacitor values from and to 3 digit codes(si format)",
    long_description=open('readme.md').read(),
    long_description_content_type="text/markdown",
    license="GPLv3",
    keywords="resistor cap capacitor digit si",
    url="https://github.com/ljurk/si_cli",
    entry_points={
        'console_scripts': ['si=si_cli.si_cli:cli']
    },
    install_requires=[
        "Click",
        "si-prefix"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
    ]
)
