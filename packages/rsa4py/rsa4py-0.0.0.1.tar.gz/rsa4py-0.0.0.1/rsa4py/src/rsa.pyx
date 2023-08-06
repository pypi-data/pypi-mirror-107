# distutils: language = c++

cimport rsa_cppInter as interface
from numpy import array, append
from numpy cimport ndarray
from libcpp.memory cimport shared_ptr
from pickle import dump, load

class InitializationError(Exception):
    """exception thrown when no sutable initiation was found"""


cdef class PublicKey:
    """rsa public encription key
    
        takes either a Public key or 2 intagers (modbaise, encription key)"""
    cdef shared_ptr[interface.PublicKey] ptr

    def __cinit__(self, *args):
        cdef PublicKey key
        cdef int p, q
        cdef interface.PublicKey* objct
        if len(args) == 1:
            key = args[0]
            self.ptr.swap(key.ptr);

        elif len(args) == 2:
            p, q = args[0], args[1]
            objct = new interface.PublicKey(p, q)
            self.ptr.reset(objct)

        else:
            raise InitializationError(f"could not initialze PublicKey with args {args} args must be Public key or 2 intagers")
    
    @property
    def n(self):
        """modular baiseis aka all operations are mod n"""
        return self.ptr.get().n
    
    @n.setter
    def n(self, val):
        self.ptr.get().n = val
    
    @property
    def e(self):
        "encription key"
        return self.ptr.get().e
    
    @e.setter
    def e(self, val):
        self.ptr.get().e = val

    cpdef encript(self, str msg):
        """encript a text
            msg is a string containing the text to encript"""
        cdef ndarray arr = array([ord(x) for x in list(msg)])
        cdef interface.cvector[long long] vec = self.ptr.get().intencript(arr)
        return array(vec)
    
    def __str__(self):
        return f"Public RSA key<e: {self.e}, n: {self.n}>"
    __repr__ = __str__

    def save(self, filename):
        assert isinstance(filename, str), f"parameter filename must be a string not {type(filename).__name__}"
        dump(["public", (self.n, self.e)], open(f"{filename}.rsa.p", "wb"))
    

cdef class PrivateKey(object):
    """private key used for both encription and decription"""
    cdef shared_ptr[interface.PrivateKey] ptr

    def __cinit__(self, *args):
        cdef PrivateKey key
        cdef int p, q, e
        cdef interface.PrivateKey* objct

        if len(args) == 0:
            objct = new interface.PrivateKey()
            self.ptr.reset(objct)

        elif len(args) == 1:
            key = args[0]
            self.ptr.swap(key.ptr);

        elif len(args) == 2:
            p, q = args[0], args[1]
            objct = new interface.PrivateKey(p, q, 0)
            self.ptr.reset(objct)
        
        elif len(args) == 3:
            p, q, e = args[0], args[1], args[2]
            objct = new interface.PrivateKey(p, q, e)
            self.ptr.reset(objct)
        


        else:
            raise InitializationError(f"could not initialze Private key with args {args} args must be Private key or 2 intagers")

    cpdef encript(self, str msg):
        """encript a text
            msg is a string containing the text to encript"""

    
        cdef ndarray arr = array([ord(x) for x in list(msg)])
        cdef interface.cvector[long long] vec = self.ptr.get().intencript(arr)
        return array(vec)

    cpdef str decript(self, crypto):
        """decript a list of values from crypto form as list of values"""
        if not isinstance(crypto, ndarray):
            crypto = array(crypto)
        cdef interface.cvector[int] keys = self.ptr.get().intdecript(crypto)
        cdef int key
        res = []
        for key in keys:
            res.append(chr(key))

        return "".join(res)
    
    @property
    def n(self):
        return self.ptr.get().n
    
    @n.setter
    def n(self, val):
        self.ptr.get().n = val
    
    @property
    def e(self):
        return self.ptr.get().e
    
    @e.setter
    def e(self, val):
        self.ptr.get().e = val
    
    @property
    def d(self):
        return self.ptr.get().d
    
    @d.setter
    def d(self, val):
        self.ptr.get().d = val
    
    def getPublic(self):
        return PublicKey(self.n, self.e)

    def save(self, filename):
        assert isinstance(filename, str), f"parameter filename must be a string not {type(filename).__name__}"
        dump(["private", (self.n, self.e, self.d)], open(f"{filename}.rsa.p", "wb"))
    
    def __str__(self):
        return f"Private RSA key<encriptonKey: {self.e}, decriptionKey: {self.d}, mod: {self.n}>"
    __repr__ = __str__


def loadKey(filename):
    assert isinstance(filename, str), f"parameter filename must be a string not {type(filename).__name__}"
    data = load(open(f"{filename}.rsa.p", "rb"))
    if data[0] == "private":
        res = PrivateKey()
        res.n, res.e, res.d = data[1]
    
    else:
        res = PublicKey(*data[1])
    return res