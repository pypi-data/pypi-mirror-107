cimport rsa_cppInter as interface
from libcpp.memory cimport shared_ptr
from numpy cimport ndarray


cdef class PublicKey:
    cpdef encript(self, str msg)
    cdef getSignature(self, str msg)
    cdef bint _SignatureCorrect(self, long long val, str string)


cdef class PrivateKey(object):
    cpdef encript(self, str msg)
    cpdef str decript(self, crypto)
    cpdef bint _SignatureCorrect(self, long long val, str string):
    cpdef getSignature(self, msg)

    cpdef test(self, int val)