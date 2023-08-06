from setuptools import setup, find_packages

requirements = []
with open('requirements.txt') as f:
    requirements = f.readlines()

setup(
    name='adolet-db',
    packages=find_packages(),
    version='0.1.5',
    license='MIT',
    description='API for AdoletDB',
    author='Adolet',
    author_email='support@adolet.com',
    url='https://github.com/adolet/adolet-db/',
    download_url=
    'https://github.com/adolet/adolet-db/archive/refs/tags/v0.1.5.tar.gz',
    keywords=['Adolet', 'Adolet DB', 'Adolet ORM'],
    install_requires=requirements,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
