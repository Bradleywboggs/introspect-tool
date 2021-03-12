from setuptools import find_packages, setup

# exec(compile(open('fm_dataout/version.py').read(),
#              'fm_dataout/version.py', 'exec'))

setup(
    name="introspect",
    version=0.1,
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    install_requires=[],
    extras_require={},
    include_package_data=True,
    description="Python library for Exporting Data from Farmobile DataEngine",
    entry_points={"console_scripts": ["analyse=introspect.main:main"]},
)
