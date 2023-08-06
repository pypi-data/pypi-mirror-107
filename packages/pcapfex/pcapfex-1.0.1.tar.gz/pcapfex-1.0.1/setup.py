from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='pcapfex',
    version='1.0.1',
    description='Extract file from pcap file',
    # long_description=str(open(path.join(here, "Pcap file extractor")).read()),
    # The project's main homepage.
    url='https://github.com/123zoeyyy/pcap_file_extractor.git',
    # Author details
    author='123zoeyyy',
    author_email='yzou10@uoguelph.ca',
    # Choose your license
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: System :: Logging',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    packages=find_packages(),
    install_requires=['regex', "dpkt"]
)
