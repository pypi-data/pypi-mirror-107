from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name="pycoord",
    version='0.0.4',
    author="KermitPurple (Shane McDonough)",
    description='Store and manipulate cartesian coordinates easier',
    long_description_content_type="text/markdown",
    long_description=long_description,
    py_modules=['pycoord'],
    package_dir={'': 'src'},
    install_requires=[],
    keywords='2D coordinate',
    url="https://github.com/KermitPurple/pycoord",
    license='MIT',
)
