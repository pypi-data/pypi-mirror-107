cimport rsa_cppInter as interface
from libcpp.memory cimport shared_ptr
from numpy cimport ndarray


cdef class PublicKey:
    cpdef encript(self, str msg)


cdef class PrivateKey(object):
    cpdef encript(self, str msg)
    cpdef str decript(self, crypto)