from setuptools import setup, find_packages


setup(name='exclude_nets',
    version='0.1.1',
    url='https://github.com/kerryeon/exclude-nets',
    author='kerryeon',
    author_email='great.ho.kim@gmail.com',
    description='Exclude the given IPv4 networks.',
    packages=find_packages(exclude=['tests']),
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[],
    entry_points={
        'console_scripts': {
            'exclude-nets = exclude_nets:main'
        }
    },
    zip_safe=False,
    classifiers=[
        'License :: OSI Approved :: MIT License'
    ],
)
