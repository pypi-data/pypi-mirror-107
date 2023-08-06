from setuptools import setup, find_packages, Extension
from Cython.Build import cythonize
from numpy import get_include
from os import system, walk

from os.path import join

cpps = []
for root, dirs, files in walk(u"rsa4py\\src\\src"):
    for file in files:
        print(file)
        if file.endswith('.cpp'):
            cpps.append(join(root, file))


libs = [u"rsa4py\\src\\lib\\rsa00.lib"]
include = ["rsa4py/src/src"]

cppLibs = [
    ("rsa4py.src.lib.rsa00",
        {
            "sources": cpps,
            "include_dirs": include,
        }
    ),
]

extensions = cythonize(  [Extension("rsa4py.src.rsa",
                                    [
                                        "rsa4py/src/rsa.pyx",
                                        "rsa4py/src/src/rsa.cpp"
                                    ],
                                    libraries = libs,
                                    include_dirs=[
                                        get_include(),
                                    ] + include,
                                    )])


setup(
    name = "rsa4py",
    packages = ["rsa4py"],
    version="0.0.0.0",
    license="apache-2.0",

    include_package_data = True,

    author = 'Julian Wandhoven',
    author_email = 'julian.wandhoven@gmail.com',

    description="python implementation of the rsa algorythem",

    long_description ="comming soon",
    
    keywords=["rsa", "Cryptography"],

    install_requires=[
        "numpy"
    ],

    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Security :: Cryptography ",
        "Programming Language :: Python :: 3",
],

    ext_modules=extensions,
    #libraries=cppLibs,
)