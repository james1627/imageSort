import os, cv2, shutil, datetime
from skimage.measure import compare_ssim
from PIL import Image
import exifread

def get_images():
	files = os.listdir('.')
	images = []
	for file in files:
		if '.' in file and '.py' not in file:
			images.append(file)
	return images


def get_date_taken(fn):
	try:
		with open(fn, 'rb') as fh:
			tags = exifread.process_file(fh, stop_tag="EXIF DateTimeOriginal")
			dateTaken = tags["EXIF DateTimeOriginal"].values
			dateTaken = dateTaken[5:7]+"-"+dateTaken[:4]
		print(dateTaken)
	except:
		print("x")
		date = datetime.datetime.fromtimestamp(os.path.getmtime(fn))
		dateTaken = str(date.month)+"-"+str(date.year)
	return dateTaken


def create_images(sources):
	images = []
	for image in sources:
		try:
			images.append(cv2.cvtColor(cv2.imread(image), cv2.COLOR_BGR2GRAY))
		except:
			print("x")
	return images

def get_removes(images):
	remove = []
	for i in range(len(images)):
	    for j in range(i + 1, len(images)):
	    	if images[i].shape[:2] == images[j].shape[:2] and compare(images[i], images[j]):
	        	remove.append(j)
	    images[i] = None
	return remove

def compare(item1, item2):
	(score, diff) = compare_ssim(item1, item2, full=True)
	diff = (diff * 255).astype("uint8")
	if score == 1:
		return True
	return False

def move_to(File, newDir):
	path = os.getcwd()+"\\"
	try:
		shutil.move(path+File, path+newDir+"\\"+File)
	except:
		os.mkdir(path+newDir)
		shutil.move(path+File, path+newDir+"\\"+File)

while(True):
	imageSources = get_images()[:10]
	if not imageSources:
		break
	remove = set(get_removes(create_images(imageSources)))

	final = []

	for i in range(len(imageSources)):
		if i in remove:
			move_to(imageSources[i],"Delete")
		else:
			newDir = get_date_taken(imageSources[i])
			move_to(imageSources[i], newDir)