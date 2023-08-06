from libcpp.vector cimport vector as cvector



cdef extern from "src/rsa.h" namespace "RSA":
    cppclass PublicKey:
        long n
        long e

        PublicKey(int n, int e)
        cvector[long long] intencript(cvector[int] msg)
    
    cppclass PrivateKey(PublicKey):
        long d
        PrivateKey(int p, int q, int e)
        PrivateKey()
        cvector[int] intdecript(cvector[long long] crypto)