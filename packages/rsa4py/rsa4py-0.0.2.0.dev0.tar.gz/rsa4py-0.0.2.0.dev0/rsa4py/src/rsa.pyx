# distutils: language = c++

cimport rsa_cppInter as interface
from numpy import array, append, ndarray
from numpy cimport ndarray
from libcpp.memory cimport shared_ptr
from pickle import dump, load
from hashlib import md5

class RSAError(Exception):
    """basic rsa4py Error"""

class InitializationError(RSAError):
    """exception thrown when no sutable initiation was found"""

class incorrectSignatureError(RSAError):
    """exception thrown when a signature is incorrect"""

cpdef long long _hash(str string, long long n):
    return int(md5(string.encode()).hexdigest(), 16)%n

cdef class CritptoMessage(list):
    """a class Reperesenting the encripted message"""
    cdef str pureText
    def __init__(self, txt, pureText=None):
        super(CritptoMessage, self).__init__(txt)
        self.signature = -1
        self.pureText = pureText
    
    def sign(self, key):
        "sign the message using a private key"
        assert isinstance(key, PrivateKey), f"key must be a private key not {type(key).__name__}"
        self.signature = key.getSignature(self.pureText)
    
    def signatureCorrect(self, key):
        assert isinstance(key, (PublicKey, PrivateKey)), f"key must be a public or private key not {type(key).__name__}"
        return key.SignatureCorrect(self, self.pureText)
    
    def save(self, str filename):
        dump(self, open(f"{filename}.msg.p", "wb"))
    
    def __str__(self):
        return f"critoText<encipted: {list(self)}, signature: {hex(self.signature)}, pureText: {self.pureText}>"
    

    def __getstate__(self):
        return [list(self), self.signature]
    
    def __setstate__(self, state):
        list.__setstate__(self, state[0])
        self.signature = state[1]
    


    
cpdef loadMsg(str filename):
    data = load(open(f"{filename}.msg.p", "rb"))

    res = CritptoMessage(data[0])
    res.signature = data[1]
    return res





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
        return CritptoMessage(array(vec), msg)
    
    def __str__(self):
        return f"Public RSA key<e: {self.e}, n: {self.n}>"
    __repr__ = __str__

    def save(self, filename):
        assert isinstance(filename, str), f"parameter filename must be a string not {type(filename).__name__}"
        dump(["public", (self.n, self.e)], open(f"{filename}.rsa.p", "wb"))
        
    cdef bint _SignatureCorrect(self, long long val, str string):
        return self.ptr.get().isSigned(val)%self.n == _hash(string, self.n)
    
    def SignatureCorrect(self, msg, string):
        """compares a messages signature with its decripted message."""
        assert isinstance(msg, CritptoMessage), f"param msg must be a CritptoMessage not {type(msg).__name__}"
        assert isinstance(string, str), f"param string must be a String not {type(str).__name__}"
        return self._SignatureCorrect(msg.signature, string)
    

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

    cpdef getSignature(self, str msg):
        "get the signature key of a a message"
        return self.ptr.get().getSignature(_hash(msg, self.n))

    cpdef encript(self, str msg):
        """encript a text
            msg is a string containing the text to encript"""

    
        cdef ndarray arr = array([ord(x) for x in list(msg)])
        cdef interface.cvector[long long] vec = self.ptr.get().intencript(arr)
        return CritptoMessage(array(vec), msg)

    cpdef str decript(self, msg, bint exception=True):
        """decript a list of values from crypto form as list of values
        
            if exception is True an exeption will be thrown if the signature is incorrect. this onwly works if the msg is a CritptoMessage."""
        if not isinstance(msg, ndarray):
            crypto = array(msg)
        else:
            crypto = msg

        cdef interface.cvector[int] keys = self.ptr.get().intdecript(crypto)
        cdef int key
        res = []
        for key in keys:
            res.append(chr(key))
        
        if isinstance(msg, CritptoMessage):
            msg.pureText = "".join(res)

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

    cpdef bint _SignatureCorrect(self, long long val, str string):
        return self.ptr.get().isSigned(val) == _hash(string, self.n)
    
    def SignatureCorrect(self, msg, string):
        """compares a messages signature with its decripted message."""
        assert isinstance(msg, CritptoMessage), f"param msg must be a CritptoMessage not {type(msg).__name__}"
        assert isinstance(string, str), f"param string must be a String not {type(str)}"
        return self._SignatureCorrect(msg.signature, string)

    cpdef test(self, int val):
        return self.ptr.get().test(val)


def loadKey(filename):
    assert isinstance(filename, str), f"parameter filename must be a string not {type(filename).__name__}"
    data = load(open(f"{filename}.rsa.p", "rb"))
    if data[0] == "private":
        res = PrivateKey()
        res.n, res.e, res.d = data[1]
    
    else:
        res = PublicKey(*data[1])
    return res