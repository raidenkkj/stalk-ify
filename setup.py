from setuptools import setup, find_packages

setup(
    name='stalk-ify',
    version='1.0.0.dev0',
    description='A tool that uses the instaloader library to increase your stalking level.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/raidenkkj/stalk-ify',
    author='Raiden Ishigami',
    author_email='contact.raidenishi69@gmail.com',
    license='GPL-3.0',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
    ],
    keywords='instagram, stalking, instaloader',
    packages=find_packages(),
    python_requires='>=3.8',
    install_requires=[
        'instaloader>=4.11',
        'colorama>=0.4.6',
        'configparser>=7.1.0',
    ],
    entry_points={
        'console_scripts': [
            'stalkify=src.__main__:main',
        ],
    },
)