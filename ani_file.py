from chunk import Chunk
import builtins

class ani_read:
    def initfp(self, file):
        pass

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

my_ani = builtins.open(".\\test_res\\lamy_wait.ani", 'rb')
chunk = Chunk(my_ani, bigendian = 0)

print(chunk.chunkname)
print(chunk.read())