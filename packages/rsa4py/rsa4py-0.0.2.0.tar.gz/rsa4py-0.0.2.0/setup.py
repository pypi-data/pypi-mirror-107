from setuptools import setup, find_packages, Extension
from os import system, walk
from sys import executable, argv

def install_Package(name):
    system(f"{executable} -m pip install {name}")
    
def upgrade_Package(name):
    system(f"{executable} -m pip install {name} --upgrade")


upgrade_Package("Cython")
upgrade_Package("numpy")

from Cython.Build import cythonize
from numpy import get_include


from os.path import join

cpps = []
for root, dirs, files in walk(u"rsa4py\\src\\src"):
    for file in files:
        if file.endswith('.cpp'):
            cpps.append(join(root, file))


include = ["rsa4py/src/src"]

extensions = cythonize(  [Extension("rsa4py.src.rsa",
                                    [
                                        "rsa4py/src/rsa.pyx",
                                        "rsa4py/src/src/rsa.cpp"
                                    ],
                                    include_dirs=[
                                        get_include(),
                                    ] + include,
                                    )])


setup(
    name = "rsa4py",
    packages = ["rsa4py"],
    version="0.0.2.0",
    license="apache-2.0",

    include_package_data = True,

    author = 'Julian Wandhoven',
    author_email = 'julian.wandhoven@gmail.com',

    description="python implementation of the rsa algorythem",

    long_description = open("README.md", "r").read(),
    long_description_content_type='text/markdown',
    
    keywords=["rsa", "Cryptography"],

    install_requires=[
        "numpy",
        "Cython",
    ],

    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Security :: Cryptography ",
        "Programming Language :: Python :: 3",
],

    ext_modules=extensions,
)