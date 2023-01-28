.ani file reader and writer for python
Currently only reader is implemented. Better-ish documentation is coming

Open ANI file with:
    f = ani_file.open(file,mode)
    
    file can be name of file or an open file
    mode is either "r", "rb" for read or "w", "wb" for write

READER:
    Available getters:
        getframesinfo() (not implemented): dictionary of info about number of frames, display sequence of frames, display rate of frames
        getnframes(): return number of frames
        getseq: return list of sequence in which the frames appear
        getrate: return list of display rate for each frame
        getframedata: return binary data of each frame

        getauthor: Get name of artist/corporation if present
        getname: Get ani file name if present

    Save frames of ani into .ico files:
        getframestofile(outputpath, filenameprefix): Save frames into .ico files at specified outputpath. Name of each file is filenameprefix + frame number (starting from 0)

#Code based on wave.py at https://github.com/python/cpython/blob/3.10/Lib/wave.py