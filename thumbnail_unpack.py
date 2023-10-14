import os
import sys
import numpy as np
from PIL import Image

'''
This script extract the image contains in .thumbnail files 
Particularly in Huawei Y7 at \sdcard\DCIM\Camera\cache\latest\

File structure:
	---------------------------------------
	|(header) 16-bytes | (payload) *-bytes]
	---------------------------------------

	Header
	------
	8th byte = image W
	9th byte = image W >> 8
	12th byte = image H
	13th byte = image H >> 8
    
Reference:
	Firmware: Huawei GM Metal TRT-LX3 TRT-L03 - 7.0.0 r1 EMUI5.1.3 05014SJR (Huawei Y7)
	app: com.huawei.camera (v40101)
	class: com.huawei.camera2.storageservice
	methods: byte[] createHeader(Bitmap bitmap); void write(Bitmap bitmap, String fileName)
'''

try:
	thumbnail = sys.argv[1]
except Exception as e:
	print("thumbnail_unpack.py IMG_xxxxxxxx_xxxxxx.thumbnail")
	exit()

filesize = os.stat(thumbnail).st_size 
print("\nFile size", filesize)

f_thumb = open(thumbnail,'rb')
thumb_byte = f_thumb.read()

img_h_index = 12
img_w_index = 8
img_h_index_rshift = 13
img_w_index_rshift = 9

w = thumb_byte[img_w_index]
h = thumb_byte[img_h_index]
w_rshift = thumb_byte[img_w_index_rshift]
h_rshift = thumb_byte[img_h_index_rshift]

if h >> 8 == h_rshift and w >> 8 == w_rshift:
	width = (w_rshift << 8) + w
	height = (h_rshift << 8) + h
	dataLen = width * height * 4
	if dataLen + 16 != filesize:
		print("Warning! Corruppted thumbnail")
else:
	print("Something Wrong")
	exit()

image_data = np.frombuffer(thumb_byte[16:], dtype=np.uint8).reshape(height, width, 4)
image = Image.fromarray(image_data)

base_file = os.path.basename(thumbnail)
output_img = os.path.splitext(base_file)[0] + ".png"

image.save(thumbnail.replace(base_file, output_img))


