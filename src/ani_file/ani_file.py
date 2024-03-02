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

        #Checks for proper .ani file
        self._has_anih_chunk = False

        #loop through each chunk
        while 1:
            try:
                chunk = Chunk(self._file, bigendian = 0)
            except EOFError:
                break

            chunkname = chunk.getname()

            if chunkname == b'anih':
                self._read_anih_chunk(chunk)
                self._has_anih_chunk = True
            #Got 2 kinds of LIST chunks: 'INFO' and 'fram'
            elif chunkname == b"LIST":
                listname = chunk.read(4)
                if listname == b"INFO":
                    self._read_info_chunk(chunk)
                elif listname == b"fram":
                    self._frames = self._read_fram_chunk(chunk)
            elif chunkname == b"seq ":
                self._read_seq_chunk(chunk)
            elif chunkname == b"rate":
                self._read_rate_chunk(chunk)
            else:
                print(f"Skipping {chunkname} chunk as not it is not part of a typical .ani file structure" )
            chunk.skip()
            
        #Check for proper .ani file
        if not self._has_anih_chunk:
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
    
    #TODO: Not sure if these 3 are really needed. Might want to brush up on python class
    def __del__(self):
        self.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    #
    # User visible method
    #

    def getfp(self):
        return self._file

    #TODO: fill this in
    def getframesinfo():
        pass

    def close(self):
        self._file = None
        file = self._i_opened_the_file
        if file:
            self._i_opened_the_file = None
            file.close()

    def getnframes(self):
        return self._nFrames

    def getauthor(self):
        return self._iart if hasattr(self,"_iart") else "no author data is included in the file"

    def getname(self):
        return self._inam if hasattr(self,"_inam") else "no name is included in the file"

    def getseq(self):
        #If no seq chunk then default seq is by frame order
        return self._seq if hasattr(self,"_seq") else [i for i in range(self._nFrames)]

    def getrate(self):
        #If no rate chunk then all frame uses default rate iDispRate
        return self._rate if hasattr(self,"_rate") else self._iDispRate
        
    def getframesdata(self):
        return self._frames

    def saveframestofile(self, outputpath=".\\", filenameprefix=""):
        for id, frame in enumerate(self._frames):
            path = outputpath+"\\"+filenameprefix+str(id)+".ico"
            new_frame = builtins.open(path, "wb")
            new_frame.write(frame)
            new_frame.close()

    #
    # Internal methods
    #

    def _read_anih_chunk(self, chunk):
        try:
            cbSize, self._nFrames, self._nSteps, self._iWidth, self._iHeight, self._iBitCount, self._nPlanes, self._iDispRate, self._bfAttributes = struct.unpack_from("<9I", chunk.read(36))
        #TODO: look into what this except actually means
        except struct.error:
            raise EOFError from None

        #TODO: might want to put some checks

    #TODO: THIS HAS NOT BEEN TESTED SINCE I DONT HAVE ANY .ANI FILE WITH INFO CHUNK
    def _read_info_chunk(self, chunk):
        while 1:
            try:
                chunk = Chunk(chunk, bigendian=0)
            except EOFError:
                break

            if chunk.getname() == b"INAM":
                self._inam = chunk.read(chunk.getsize()).decode("utf-8")
            elif chunk.getname() == b"IART":
                self._iart = chunk.read(chunk.getsize()).decode("utf-8")

            chunk.skip()
    
    def _read_fram_chunk(self, chunk):
        #TODO: support bitmaps frames
        if (self._bfAttributes!=3 and self._bfAttributes!=1):
            raise Exception("Frame info is in bitmaps (instead of ico) which is not supported for now")
            
        frames = list()
        while 1:
            try:
                frame_chunk = Chunk(chunk, bigendian = 0)
            except EOFError:
                break

            frames.append(frame_chunk.read(frame_chunk.getsize()))
            frame_chunk.skip()
        return frames

    def _read_seq_chunk(self, chunk):
        self._seq = tuple()
        for i in range(self._nSteps):
            self._seq += struct.unpack_from("I", chunk.read(4))

    def _read_rate_chunk(self, chunk):
        self._rate = tuple()
        for i in range(self._nSteps):
            self._rate += struct.unpack_from("I", chunk.read(4))

class ani_write:
    def __init__(self, f):
        self._i_opened_the_file = None
        if isinstance(f, str):
            f = builtins.open(f, 'wb')
            self._i_opened_the_file = f
        try:
            self.initfp(f)
        except:
            if self._i_opened_the_file:
                f.close()
            raise
    
    def initfp(self, file):
        self._file = file

        self._nFrames = 0
        self._nSteps = 0
        self._iDispRate = 8 #Default rate 8 jiffy
        self._bfAttributes = 1 # 1 = no seq chunk; 3 = got seq chunk
        #These four are only non-zeroes if images are in bitmaps
        self._iWidth = 0
        self._iHeight = 0
        self._iBitCount = 0
        self._nPlanes = 0

        self._framespath = []
        self._datawritten = 0

    def __del__(self):
        self.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    #
    # User visible method
    #

    def setframespath(self, framespath):
        self._framespath = framespath
        self._nFrames = len(framespath)
        if (not hasattr(self,"_nSteps")): self._nSteps = len(framespath)

    def setseq(self, seq):
        self._seq = seq
        self._bfAttributes = 3
        self._nSteps = len(seq)
    
    def setrate(self, rate):
        if isinstance(rate,int):
            self._iDispRate = rate
            self._rate = None
        else:
            self._rate = rate

    def setauthor(self, iart):
        self._iart = iart.encode("utf-8")
    
    def setname(self, inam):
        self._inam = inam.encode("utf-8")

    def close(self):
        try:
            if self._file:
                self._write_data()
                self._file.flush()
        finally:
            self._file = None
            file = self._i_opened_the_file
            if file:
                self._i_opened_the_file = None
                file.close()
    
    #
    # Internal methods.
    #

    def _write_data(self):
        #Pack these chunks first to calculate _datawritten correctly
        anih = self._pack_anih()
        info = self._pack_info()
        rate = self._pack_rate()
        seq = self._pack_seq()
        frames = self._pack_frames()

        self._file.write(struct.pack("<4sI4s",b"RIFF",4+self._datawritten,b"ACON") + anih + info + rate + seq + frames)

    def _pack_info(self):
        if hasattr(self,"_inam") or hasattr(self,"_iart"):
            inamChunk,iartChunk = b"",b""
            # IMPORTANT: _inam and _iart need to be padded to even length for Chunk to work
            if hasattr(self,"_inam"):
                inamChunk = struct.pack(f'<4sI{len(self._iart)}s{"x"*(len(self._inam)%2)}' ,b"INAM",len(self._inam),self._inam)
            if hasattr(self,"_iart"):
                iartChunk = struct.pack(f'<4sI{len(self._iart)}s{"x"*(len(self._iart)%2)}',b"IART",len(self._iart),self._iart)
            
            self._datawritten += 12 + len(iartChunk) + len(inamChunk)
            return struct.pack("<4sI4s", b"LIST",4+len(inamChunk)+len(iartChunk),b"INFO") + inamChunk + iartChunk

        
    def _pack_frames(self):
        iconSize = 0
        iconChunks = b""

        for framPath in self._framespath:
            with builtins.open(framPath, "rb") as icon:
                data = icon.read()
                iconChunks += struct.pack("<4sI",b"icon",len(data)) + data
                iconSize += 8 + len(data)
                
        self._datawritten += 12 + iconSize
        return struct.pack("<4sI4s", b"LIST",4+iconSize,b"fram") + iconChunks

    def _pack_anih(self):
        self._datawritten += 44 #Size of 11I of anih chunk
        return struct.pack("<4s10I",b"anih",36,36,self._nFrames,self._nSteps,self._iWidth,self._iHeight,self._iBitCount,self._nPlanes,self._iDispRate,self._bfAttributes)

    def _pack_rate(self):
        if hasattr(self,"_rate"):
            self._datawritten += 8+4*len(self._rate)
            return struct.pack(f"<4sI{len(self._seq)}I", b"rate",4*len(self._rate),*self._rate)

    def _pack_seq(self,):
        if hasattr(self,"_seq"):
            self._datawritten += 8+4*len(self._seq)
            return struct.pack(f"<4sI{len(self._seq)}I", b"seq ",4*len(self._seq),*self._seq)
    
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