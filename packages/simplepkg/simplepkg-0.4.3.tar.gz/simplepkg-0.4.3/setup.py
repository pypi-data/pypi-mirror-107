import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='simplepkg',
    version='0.4.3',
    author='Brandon Nunez',
    author_email='b@bnunez.com',
    description='Simple python package scaffolding utility.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/b5n/simplepkg',
    packages=setuptools.find_packages(
        exclude=['test', '*.test', '*.test.*', 'test.*', ]),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
    include_package_data=True,
    install_requires=[
        'setuptools',
        'pathlib',
    ],
    entry_points={
        'console_scripts': [
            'simplepkg=simplepkg.__main__:main',
        ]
    },
)
