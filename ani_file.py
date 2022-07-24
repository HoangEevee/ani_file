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

            chunkname = chunk.getname()
            if chunkname == b"anih":
                self._read_anih_chunk(chunk)
            elif chunkname == b"LIST":
                self._list_chunk = chunk

            print(chunkname)
            chunk.skip()
        

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

    def _read_anih_chunk(self, chunk):
        pass

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

