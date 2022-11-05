import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

packages = [
    'discord'
]

setuptools.setup(
    name='kuro-bot',
    version='1.3.0',
    packages=packages,
    author='Juliana Diaz',
    description='Basic informational Bot of Shoujo Kageki Revue Starlight franchise',
    long_description=long_description,
    python_requires='>=3.7'
)
