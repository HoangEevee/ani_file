# ani_file 
.ani file (animated cursor) reader and writer written in python 3.

Was trying to batch extract the frames of some .ani file I got but noticed that there were no library to do so in python so I created one. 

## Starting point
Clone this repo or download package from Pypi with `pip install ani_file`:

Open ANI file in similar manner to builtin.open():
```
    from ani_file import ani_file
    f = ani_file.open(file,mode)
```
`file` can be string or file-like object.

mode can be:
`"r"` or `"rb"` to read an existing .ani file.
`"w"` or `"wb"` to create a new .ani file. **Will overwrite existing file if there is one**

## Read .ani
### Available getter:

`getframesinfo()` (**NOT IMPLEMENTED YET**): dictionary of info about number of frames, display sequence of frames, display rate of frames

`getnframes()`: return number of frames

`getseq()`: return list of sequence in which the frames appear

`getrate()`: return list of display rate for each frame

`getframesdata()`: return list of binary data of each frame

`getauthor()`: Get name of artist/corporation if present

`getname()`: Get ani file name (Not the name of the .ani file) if present

### Extract and save frames into .ico files:

`saveframestofile(outputpath,filenameprefix)`: Save to specified path. Name of each file will be filenameprefix + index from 0

## Write .ani
### Available getter (**NOT IMPLEMENTED YET**):
Same as for read .ani

### Available setter:

`setframespath(framespath)`: set list of .ico files that make the frames of the final .ani file. The only function that you really need to write an .ani file

`setseq(seq)`: set seq 

`setrate(rate)`: set rate

`setauthor(iart)`: set name of artist

`setname(inam)`: set name of the ani file

### Example (**INCOMING**)

### .ani file structure explain (**INCOMING**)



Code based on wave.py at https://github.com/python/cpython/blob/3.10/Lib/wave.py
