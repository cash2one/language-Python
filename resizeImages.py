from PIL import Image
import os

MAX_SIZE = 2048

def resize(imageName):
	img = Image.open(imageName)
	width = img.size[0] if img.size[0] <= MAX_SIZE and img.size[1] <= MAX_SIZE else MAX_SIZE if img.size[0] > img.size[1] else MAX_SIZE * img.size[0] / img.size[1]
	height = img.size[1] if img.size[0] <= MAX_SIZE and img.size[1] <= MAX_SIZE else MAX_SIZE * img.size[1] / img.size[0] if img.size[0] >= img.size[1] else MAX_SIZE
	print '( W', width, '/ H', height, ')',
	resized_img = img.resize((width, height), Image.ANTIALIAS)
	basename, extension = os.path.splitext(imageName)
	resized_img.save(basename + '_new.jpg')

def getJpgList():
	imgList = os.listdir(os.path.abspath(os.curdir))
	result = []
	for imgName in imgList:
		basename, extension = os.path.splitext(imgName)
		if extension.lower() in ['.jpg', 'jpeg']:
			result.append([basename, extension])
	return result

if __name__ == '__main__':
	lists = getJpgList()
	count = len(lists)
	if count == 0:
		print 'no .jpg file found.'
		exit()
	ind = 1

	for n, x in lists:
		print '[', ind, '/', count, ']', n + x,
		resize(n + x)
		print 'was resized successfully.'
		ind += 1
