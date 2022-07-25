from chunk import Chunk
import builtins
import struct

class ani_read:
    def initfp(self, file):
        self._file = Chunk(file, bigendian = 0)

        #Check if file is an .ani file
        if self._file.getname() != b"RIFF":
            raise Exception("file does not start with RIFF id")
        if self._file.read(4) != b"ACON":
            raise Exception("not an .ANI file")

        #loop through each chunk
        while 1:
            try:
                chunk = Chunk(self._file, bigendian = 0)
            except EOFError:
                break

            #Checks for proper .ani file
            self._has_anih_chunk = False
            self._has_fram_chunk = False

            chunkname = chunk.getname()
            print(chunkname)

            if chunkname == b'anih':
                self._read_anih_chunk(chunk)
                self._has_anih_chunk = True
            #Got 2 kinds of LIST chunks: 'INFO' or 'fram'
            elif chunkname == b"LIST":
                listname = chunk.read(4)
                if listname == b"INFO":
                    self._info_chunk = chunk
                elif listname == b"fram":
                    self._fram_chunk = chunk
                    self._has_fram_chunk = True
            chunk.skip()

        #Check for proper .ani file
        if not self._has_anih_chunk or not self._has_fram_chunk:
            raise Exception("anih chunk and/or fram chunk missing")

    def __init__(self, file):
        self._i_opened_the_file = None
        if isinstance(file, str):
            file = builtins.open(file, 'rb')
            self._i_opened_the_file = file
        # else, assume it is an open file object already
        try:
            self.initfp(file)
        except:
            if self._i_opened_the_file:
                file.close()
            raise
    
    #TODO: Not sure if these 3 are really needed. Might want to brush up python class
    def __del__(self):
        self.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    #
    # User visible method
    #

    #
    # Internal methods
    #

    def _read_anih_chunk(self, chunk):
        try:
            cbSize, self._nFrames, nSteps, self._iWidth, self._iHeight, iBitCount, nPlanes, self._iDispRate, self._bfAttributes = struct.unpack_from("<9I", chunk.read(36))
            print(cbSize, self._nFrames, nSteps, self._iWidth, self._iHeight, iBitCount, nPlanes, self._iDispRate, self._bfAttributes)
        #TODO: look into what this except actually means
        except struct.error:
            raise EOFError from None

        #TODO: might want to put some checks
        
class ani_write:
    pass

def open(file, mode=None):
    if mode is None:
        if hasattr(file, "mode"):
            mode = file.mode
        else:
            mode = "rb"
    if mode in ("r", "rb"):
        return ani_read(file)
    elif mode in ("w", "wb"):
        return ani_write(file)
    else:
        raise Exception("Mode must be 'r', 'rb', 'w', or 'wb'")

