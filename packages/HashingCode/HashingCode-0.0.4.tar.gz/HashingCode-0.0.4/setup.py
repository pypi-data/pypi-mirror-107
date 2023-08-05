from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='HashingCode',
    version='0.0.4',
    description='A hashing library',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Abderrahman Hiroual',
    author_email='hiroual.abderrahman.student@gd-gsr.com',
    license='MIT',
    classifiers=classifiers,
    keywords='Hashing',
    packages=find_packages(),
    install_requires=['']
)