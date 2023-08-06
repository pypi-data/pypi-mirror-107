from setuptools import setup, find_packages

def readme() -> str:
    with open(r'README.md') as f:
        README = f.read()
    return README

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Intended Audience :: Financial and Insurance Industry',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='ymcntr',
    version='0.0.1',
    description='Module of basic calculations',
    long_description=readme(),
    long_description_content_type="text/markdown",
    url='https://github.com',
    author='Yam',
    author_email='ymgchbrtv0095@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords=['calculator', 'math'],
    packages=find_packages(),
    install_requires=['']
)