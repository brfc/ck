from setuptools import setup, find_packages

setup(
    name='ck',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'click',
        'pyyaml',
    ],
    entry_points={
        'console_scripts': [
            'ck=ck.cli:cli',
        ],
    },
    author='R. Carvalho',
    author_email='brfc.email@gmail.com',
    description='A tool to save and list shell commands',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/brfc/ck',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    package_data={'ck': ['conf.yaml']}, 

)
