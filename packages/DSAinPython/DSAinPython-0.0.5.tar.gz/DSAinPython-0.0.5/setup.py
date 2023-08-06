from setuptools import setup, find_packages

classifiers=[
'Development Status :: 5 - Production/Stable', 
'Intended Audience :: Education',
'Operating System :: OS Independent',
'License :: OSI Approved :: MIT License',
'Programming Language :: Python :: 3'
]

setup(
    name= 'DSAinPython', 
    version='0.0.5',
    author='Armaan Chauhan',
    author_email='armaanchauhan268@gmail.com',
    description='This Package contains Data Structures and Algorithms', 
    long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Armaan-268/DSA_in_Python',
    license="MIT",
    classifier=classifiers, 
    keywords='datastructures,algorithms',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['']
)