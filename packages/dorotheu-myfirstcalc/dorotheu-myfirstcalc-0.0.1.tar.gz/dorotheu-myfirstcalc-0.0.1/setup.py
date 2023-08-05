from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='dorotheu-myfirstcalc',
    version='0.0.1',
    description='Uma simples calculadora',
    long_description=open("README.md").read() + '\n\n' + open("CHANGELOG.txt").read(),
    url='',
    author='Danilo Dorotheu',
    author_email='danilo.dorotheu@outlook.com',
    license='MIT',
    classifiers=classifiers,
    keywords='calculator',
    packages=find_packages(),
    install_requires=['']
)
