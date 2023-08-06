import setuptools
import PathFile

with open('README.md') as fr:
    long_description = fr.read()

setuptools.setup(
    name='PathFile',
    version=PathFile.__version__,
    author='Murashkin Artem',
    author_email='artemmurashkin02@mai.ru',
    description='This package is PathFile',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ArtemMurashkin',
    packages=setuptools.find_packages(),
    install_requires=[
        'pypiwin32>=223'
    ],
    test_suite='tests',
    python_requires='>=3.0',
    platforms=["any"]
)