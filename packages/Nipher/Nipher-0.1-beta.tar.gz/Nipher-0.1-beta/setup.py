from distutils.core import setup

long_description = ""

setup(
    name='Nipher',
    packages=['src'],
    version='0.1-beta',
    license='MIT',
    description='IP lookup tool to avoid manual check.',
    long_description=long_description,
    author='Pedro Huang',
    author_email='justhuangpedro@gmail.com',
    url='https://github.com/Slyrack/Nipher',
    download_url='https://github.com/Slyrack/Nipher/archive/refs/tags/v0.1-beta.tar.gz',
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
