# ani_file 
.ani file (animated cursor) reader and writer written in python 3.

Was trying to batch extract the frames of some .ani file I got but noticed that there were no library to do so in python so I created one. 

Reader can read metadata and extract frames (into either .cur or .ico as encoded in the .ani).

Writer can create .ani from .cur, .ico, or other file types like .png as supported by Iconolatry. .cur files may be created as needed and will be stored in the same folder as the .ani file. 

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

`getframesinfo()`: return metadata in the anih header chunk

`getnframes()`: return number of frames

`getseq()`: return list of sequence in which the frames appear

`getrate()`: return list of display rate for each frame

`getframesdata()`: return list of binary data of each frame

`getauthor()`: Get name of artist/corporation if present

`getname()`: Get ani file name (Not the name of the .ani file) if present

### Extract and save frames into .ico files:

`saveframestofile(outputpath,filenameprefix)`: Save to specified path. Name of each file will be filenameprefix + index from 0

## Write .ani
### Available setter:

`setframespath(framespath,xy)`: set list of .ico/.cur files that make the frames of the final .ani file. xy is a list of the cursor's hotspot defined as offset from the top-left corner and is a property of .cur file. If framespath are not .cur files (or .ico with xy specified) then .cur file will be generated. If framespath are .cur files then xy will be ignored. 

`setseq(seq)`: set seq 

`setrate(rate)`: set rate

`setauthor(iart)`: set name of artist

`setname(inam)`: set name of the ani file

### Example 
```
    from ani_file import ani_file
    #Creating .ani file from .png
    f = ani_file.open(".\\out\\ani.ani","w")
    lists = [".\\res\\cursor0.png",
        ".\\res\\cursor1.png",
        ".\\res\\cursor2.png",]
    f.setframespath(lists,xy=(0,0))
    f.close

    #extracting frames from existing .ani file
    f = ani_file.open(".\\out\\ani.ani","r")
    f.saveframestofile(".\\out","cursor")
```
### .ani file structure explain 

https://www.informit.com/articles/article.aspx?p=1189080&seqNum=3

https://www.daubnet.com/en/file-format-ani



Code based on wave.py at https://github.com/python/cpython/blob/3.10/Lib/wave.py. Cursor converter is Iconolatry from https://github.com/SystemRage/Iconolatry/tree/master. 
