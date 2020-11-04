import numpy as np
import fire
# from scipy import misc
import imageio
import matplotlib.pyplot as plt
from scipy import signal
from skimage.filters import threshold_sauvola

def _load_gray(img):
	x = imageio.imread(img)[:,:,:3]
	x = np.linalg.norm(x, axis=2)/np.sqrt(3)
	return x


def make_template(img):
	# x = imageio.imread(img)[:,:,:3]
	# print(x.shape)
	x = _load_gray(img)
	# xsub = x[350:400,475:600]
	xsub = x[675:720,480:600]

	plt.imshow(xsub)
	plt.show()
	np.savetxt('template.txt', np.round(xsub).astype(np.int), fmt='%u')


def _find_template_in_img(x, xsub):
	# print(xsub.shape)
	# assert False
	print(x.shape)
	m = np.mean(x)
	x = x - m
	s = np.std(x)
	x = x / s
	xsub = (xsub - m)/s
	# x = x/255.0
	# xsub = xsub/255.0
	# x = 1 - x
	# xsub = 1 - xsub
	m = np.mean(xsub)
	xsub = xsub - m
	x = x - m
	z = signal.correlate(x, xsub, mode = 'valid')
	znorm = signal.correlate(np.abs(x), np.ones(xsub.shape), mode = 'valid')
	# znorm[znorm == 0] = 1
	# znorm = 1
	# print(z)
	# print(znorm)
	print(xsub)
	print('xsub')
	plt.imshow(xsub)
	plt.show()

	print('z')
	plt.imshow(z)
	plt.show()

	print('znorm')
	plt.imshow(znorm)
	plt.show()

	z = z / znorm
	print('z')
	plt.imshow(z)
	plt.show()
	# print(x.shape)
	# print(z.shape)
	# print(c)
	'''
	X = np.fft.fft2(x)
	Xsub = np.fft.fft2(xsub, X.shape)
	z = np.abs(np.fft.ifft2(np.conj(Xsub)*X))
	# z = np.fft.fftshift(z)
	'''
	# ix = np.argmax(z)
	row, col = np.unravel_index(z.argmax(), z.shape)
	#np.divmod(ix, x.shape[1])

	# row -= xsub.shape[0]/2
	# col -= xsub.shape[1]/2
	return int(np.round(row)), int(np.round(col))


def make_weather_bw(img, template, debug=False, inky=False):
	if inky:
		from inky import InkyWHAT
		inky_display = InkyWHAT("black")
		inky_display.set_border(inky_display.WHITE)
		assert inky_display.WIDTH == 400
		assert inky_display.HEIGHT == 300
	im = _load_gray(img)
	t = np.loadtxt(template)
	row, col = _find_template_in_img(im, t)
	if debug:
		plt.imshow(im, cmap='gray', vmin=0, vmax=255)
		plt.plot([col],[row], color='r',marker='x')
		plt.show()

	im = imageio.imread(img)[:,:,:3]
	# row, col, h, w
	patch_1 = [-170, -295, 190, 225]
	patch_2 = [180, -290, 110, 225]
	patches = []
	for r,c,h,w in [patch_1, patch_2]:
		y = row + r
		x = col + c
		patch =im[y:y+h,x:x+w]
		patches.append(patch)
		if debug:
			plt.imshow(patch)
			plt.show()
	patch = np.vstack(patches)
	patch = patch.astype(np.int)
	# patch[patch < 220] = patch[patch < 220] - 150
	# patch[patch > 220] = 255
	# print(patch)
	# patch -= 10
	patch = np.maximum(patch, 0)
	print(patch)
	print('############')
	print(patch.shape)
	print('############')
	plt.imshow(patch)
	plt.savefig('test.png')
	plt.close()
	from PIL import Image, ImageFont, ImageDraw
	pal_img = Image.new("P", (1, 1))
	pal_img.putpalette((255, 255, 255, 0, 0, 0) + (0, 0, 0) * 253)
	screen_size = np.array([400, 300])

	uppx = np.min(screen_size - np.array(patch.shape[:2]))
	patch_im = Image.fromarray(np.uint8(patch))
	# TODO fix aspect ratio
	patch_im = patch_im.resize((patch.shape[1]+uppx, patch.shape[0]+uppx))
	# patch_im = patch_im.quantize(palette=pal_img)
	# screen_img
	# import ipdb; ipdb.set_trace()
	# a = np.array(patch.shape[:2])

	# resize = np.max(np.array(patch.shape[:2])/np.array([400.,300.]))*np.array([400.,300.])
	# print(resize)

	screen_img = Image.new("P", (300, 400))
	screen_img.paste(patch_im)
	screen_img = screen_img.convert("RGB").quantize(palette=pal_img)
	if inky:
		inky_display.set_image(screen_img)
		inky_display.show()
	else:
		# screen_img.show()
		screen_img.save("latest.png")
	# draw = ImageDraw.Draw(screen_img)

	# thresh = threshold_sauvola(patch,k=.1, r=73.6121593217,window_size=11)
	# print(patch)
	# patch = patch > thresh
	# patch = signal.medfilt(patch, 1)
	# plt.imshow(patch, cmap='gray', vmin=0, vmax=1)
	# plt.show()
	# print(X.shape)

if __name__ == '__main__':
	fire.Fire()
