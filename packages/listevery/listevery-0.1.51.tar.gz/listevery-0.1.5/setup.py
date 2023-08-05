from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
        name='listevery',
        version='0.1.5',
        url='https://github.com/themysticsavages/listevery',
        author='themysticsavages',
        description="A file lister on steroids",
        long_description=long_description,
        long_description_content_type="text/markdown",
        author_email='noemailprovidedthankyou@nonexistentemailservice.com',
        license='Apache',
        packages=['listevery'],
        python_requires=">=3.6",

        classifiers = [
            'Programming Language :: Python :: 3',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
        ]
)