import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pmb_py-noflame",
    version="0.0.1",
    author="Noflame.lin",
    author_email="linjuang@gmail.com",
    description="pmb restful api python wrap",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MoonShineVFX/pmb_py_api",
    py_modules=['pmb_py'],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)