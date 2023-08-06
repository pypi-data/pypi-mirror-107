import numpy as np

import numba as nb
NBError=nb.errors.NumbaError
nb_uint8_ro=nb.typeof(np.frombuffer(b"\x00\x00",dtype="u1").reshape((1,2))[:,::-1]) # to create readonly any-indexing 2D u1 array argument type
nb_width=nb.typeof(np.empty([0]).shape[0]) # pylint: disable=unsubscriptable-object



def make_unpacker_3to2(ubs, rtype=nb.uint16):
    """
    Make a numba unpacker function, which converts each 3 consecutive source bytes into 2 resulting values.

    `ubs` is a list of 2 numba functions which take 3 inputs bits (already converted to `rtype`)
    and return the corresponding result values.
    `rtype` is the numba type of the resulting array, and of the values passed to `ubs`.
    """
    ub0,ub1=ubs
    @nb.njit(rtype[:,:](nb_uint8_ro,nb_width),parallel=False)
    def unpacker(raw_data, width):
        """
        Convert packed 12bit data (3 bytes per 2 pixels) into unpacked 16bit data (2 bytes per pixel).

        `raw_data` is a 2D numpy array with the raw frame data of dimensions ``(nrows, stride)``, where ``stride`` is the size of one row in bytes.
        `width` is the size of the resulting row in pixels; if it is 0, assumed to be maximal possible size.
        """
        h,s=raw_data.shape
        if width==0:
            width=(s*2)//3
        out=np.empty((h,width),dtype=rtype)
        chwidth=width//2
        for i in range(h):
            for j in range(chwidth):
                b0=rtype(raw_data[i,j*3  ])
                b1=rtype(raw_data[i,j*3+1])
                b2=rtype(raw_data[i,j*3+2])
                out[i,j*2  ]=ub0(b0,b1,b2)
                out[i,j*2+1]=ub1(b0,b1,b2)
            b0=rtype(raw_data[i,chwidth*3  ]) if s>chwidth*3   else 0
            b1=rtype(raw_data[i,chwidth*3+1]) if s>chwidth*3+1 else 0
            b2=rtype(raw_data[i,chwidth*3+2]) if s>chwidth*3+2 else 0
            if width%2==1:
                out[i,chwidth*2]=ub0(b0,b1,b2)
        return out
    return unpacker

def make_unpacker_5to4(ubs, rtype=nb.uint16):
    """
    Make a numba unpacker function, which converts each 5 consecutive source bytes into 4 resulting values.

    `ubs` is a list of 4 numba functions which take 5 inputs bits (already converted to `rtype`)
    and return the corresponding result values.
    `rtype` is the numba type of the resulting array, and of the values passed to `ubs`.
    """
    ub0,ub1,ub2,ub3=ubs
    @nb.njit(rtype[:,:](nb_uint8_ro,nb_width),parallel=False)
    def unpacker(raw_data, width):
        """
        Convert packed 10bit data (5 bytes per 4 pixels) into unpacked 16bit data (2 bytes per pixel).

        `raw_data` is a 2D numpy array with the raw frame data of dimensions ``(nrows, stride)``, where ``stride`` is the size of one row in bytes.
        `width` is the size of the resulting row in pixels; if it is 0, assumed to be maximal possible size.
        """
        h,s=raw_data.shape
        if width==0:
            width=(s*4)//5
        out=np.empty((h,width),dtype=rtype)
        chwidth=width//4
        for i in range(h):
            for j in range(chwidth):
                b0=rtype(raw_data[i,j*5  ])
                b1=rtype(raw_data[i,j*5+1])
                b2=rtype(raw_data[i,j*5+2])
                b3=rtype(raw_data[i,j*5+3])
                b4=rtype(raw_data[i,j*5+4])
                out[i,j*4  ]=ub0(b0,b1,b2,b3,b4)
                out[i,j*4+1]=ub1(b0,b1,b2,b3,b4)
                out[i,j*4+2]=ub2(b0,b1,b2,b3,b4)
                out[i,j*4+3]=ub3(b0,b1,b2,b3,b4)
            b0=rtype(raw_data[i,chwidth*5  ]) if s>chwidth*5   else 0
            b1=rtype(raw_data[i,chwidth*5+1]) if s>chwidth*5+1 else 0
            b2=rtype(raw_data[i,chwidth*5+2]) if s>chwidth*5+2 else 0
            b3=rtype(raw_data[i,chwidth*5+3]) if s>chwidth*5+3 else 0
            b4=rtype(raw_data[i,chwidth*5+4]) if s>chwidth*5+4 else 0
            if width%4>0:
                out[i,chwidth*4  ]=ub0(b0,b1,b2,b3,b4)
            if width%4>1:
                out[i,chwidth*4+1]=ub1(b0,b1,b2,b3,b4)
            if width%4>2:
                out[i,chwidth*4+2]=ub2(b0,b1,b2,b3,b4)
        return out
    return unpacker


# standard 12-bit lsb packed
@nb.njit
def u12b0(b0, b1, b2):  # pylint: disable=unused-argument
    return b0|((b1&0x0F)<<8)
@nb.njit
def u12b1(b0, b1, b2):  # pylint: disable=unused-argument
    return (b1>>4)|(b2<<4)

# standard 10-bit lsb packed
@nb.njit
def u10b0(b0, b1, b2, b3, b4):  # pylint: disable=unused-argument
    return b0|((b1&0x03)<<8)
@nb.njit
def u10b1(b0, b1, b2, b3, b4):  # pylint: disable=unused-argument
    return (b1>>2)|((b2&0x0F)<<6)
@nb.njit
def u10b2(b0, b1, b2, b3, b4):  # pylint: disable=unused-argument
    return (b2>>4)|((b3&0x3F)<<4)
@nb.njit
def u10b3(b0, b1, b2, b3, b4):  # pylint: disable=unused-argument
    return (b3>>6)|(b4<<2)

# middle-byte-grouped ("Andor-style") 12-bit packed
@nb.njit
def u12agb0(b0, b1, b2):  # pylint: disable=unused-argument
    return (b0<<4)|(b1&0x0F)
@nb.njit
def u12agb1(b0, b1, b2):  # pylint: disable=unused-argument
    return (b2<<4)|(b1>>4)



unpack12=make_unpacker_3to2([u12b0,u12b1])
unpack12ag=make_unpacker_3to2([u12agb0,u12agb1])
unpack10=make_unpacker_5to4([u10b0,u10b1,u10b2,u10b3])