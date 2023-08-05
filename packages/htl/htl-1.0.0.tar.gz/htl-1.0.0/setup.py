import setuptools
import htl


with open('README.md') as fr:
    long_description = fr.read()


setuptools.setup(
    name='htl',
    version=htl.__version__,
    author='Sidorenko Ekaterina',
    author_email='sidorenkoekaterina01@icloud.com',
    description='Library for transform data structures',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/EkaterinaSidorenko17/htl',
    packages=setuptools.find_packages(),
    install_requires=[
        
    ],
    test_suite='tests',
    python_requires='>=3.7',
    platforms=["any"]
)