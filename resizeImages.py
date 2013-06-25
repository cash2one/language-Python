from PIL import Image
import os

MAX_SIZE = 2048

def resize(imageName):
	img = Image.open(imageName)
	width = img.size[0] if img.size[0] <= MAX_SIZE and img.size[1] <= MAX_SIZE else MAX_SIZE if img.size[0] > img.size[1] else MAX_SIZE * img.size[0] / img.size[1]
	height = img.size[1] if img.size[0] <= MAX_SIZE and img.size[1] <= MAX_SIZE else MAX_SIZE * img.size[1] / img.size[0] if img.size[0] >= img.size[1] else MAX_SIZE
	print 'width:', width, 'height:', height,
	resized_img = img.resize((width, height), Image.ANTIALIAS)
	basename, extension = os.path.splitext(imageName)
	resized_img.save(basename + '_new.jpg')

if __name__ == '__main__':
	imgList = os.listdir(os.path.abspath(os.curdir))
	for imgName in imgList:
		basename, extension = os.path.splitext(imgName)
		if extension.lower() == '.jpg':
			resize(imgName)
			print imgName, 'was resized successfully.'
