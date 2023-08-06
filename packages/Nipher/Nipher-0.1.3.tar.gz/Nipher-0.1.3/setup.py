from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(
    name='Nipher',
    packages=['Nipher'],
    version='0.1.3',
    license='MIT',
    description='IP lookup tool to avoid manual check.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Pedro Huang',
    author_email='justhuangpedro@gmail.com',
    entry_points={
            'console_scripts': [
                'nipher = Nipher.__main__:main'
            ]
        },
    url='https://github.com/Slyrack/Nipher',
    download_url='https://github.com/Slyrack/Nipher/archive/refs/tags/v0.1.3.tar.gz',
    keywords=['Nipher', 'IP Lookup', 'IP Geolocation'],
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
