from chunk import Chunk
import builtins
import struct
import ani_file

ani_file.open(".\\test_res\\lamy_wait.ani")
if ani_file._
#ani_file.open(".\\test_res\\aero_busy.ani")

'''
my_ani = builtins.open(".\\test_res\\lamy_wait.ani", 'rb')


#print(my_ani.read())
whole_chunk = Chunk(my_ani, bigendian = 0)

print(whole_chunk.getname())
print(whole_chunk.getsize())
print(whole_chunk.read(4))
chunk = Chunk(whole_chunk, bigendian = 0)
print(chunk.getname())
print(chunk.getsize())
print(chunk.tell())
cbSize, nFrames, nSteps, iWidth, iHeight, iBitCount, nPlanes, iDispRate, bfAttributes = struct.unpack_from("<9I", chunk.read(36))
print(cbSize, nFrames, nSteps, iWidth, iHeight, iBitCount, nPlanes, iDispRate, bfAttributes)
print(chunk.tell())
chunk.skip()
chunk = Chunk(whole_chunk, bigendian = 0)
print(chunk.getname())
print(chunk.getsize())
icon_chunk = Chunk(chunk, bigendian = 0)
print(icon_chunk.getname())
print(struct.unpack_from("I",icon_chunk.read(4)))
#print(icon_chunk.getsize())
chunk.skip()
chunk = Chunk(whole_chunk, bigendian = 0)
print(chunk.getname())
print(chunk.getsize())
'''