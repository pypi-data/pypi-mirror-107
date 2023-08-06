from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='netframe',
    version='0.0.1',
    author='Xeronick',
    author_email='xeronick@outlook.com',
    description='NetFrame is a Python framework designed to simplify network configuration',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://www.github.com/xeronick/netframe',
	license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    py_modules=['netframe'],
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.7',
    install_requires=[
        'setuptools>=38.4.0',
		'netmiko>=3.4.0',
		'Jinja2>=3.0.0',
	]
)
