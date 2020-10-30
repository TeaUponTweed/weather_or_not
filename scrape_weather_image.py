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
	xsub = x[350:400,475:600]
	plt.imshow(xsub)
	plt.show()
	np.savetxt('template.txt', np.round(xsub).astype(np.int), fmt='%u')


def _find_template_in_img(x, xsub):
	# print(xsub.shape)
	# assert False
	z = signal.fftconvolve(x, xsub, mode = 'valid')
	znorm = signal.fftconvolve(x, np.ones(xsub.shape), mode = 'valid')
	znorm[znorm == 0] = 1

	# print(z)
	# print(znorm)
	z = z / znorm
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


def make_weather_bw(img, template, debug=False):
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
	patch[patch < 220] = patch[patch < 220] - 150
	# print(patch)
	# patch -= 10
	patch = np.maximum(patch, 0)
	print(patch)
	print('############')
	print(patch.shape)
	print('############')
	from PIL import Image, ImageFont, ImageDraw
	pal_img = Image.new("P", (1, 1))
	pal_img.putpalette((255, 255, 255, 0, 0, 0) + (0, 0, 0) * 253)
	screen_size = np.array([400, 300])
	uppx = np.min(screen_size - np.array(patch.shape[:2]))
	patch_im = Image.fromarray(np.uint8(patch))

	screen_img = patch_im.resize((patch.shape[1]+uppx, patch.shape[0]+uppx))
	screen_img = screen_img.quantize(palette=pal_img)
	# import ipdb; ipdb.set_trace()
	# a = np.array(patch.shape[:2])

	# resize = np.max(np.array(patch.shape[:2])/np.array([400.,300.]))*np.array([400.,300.])
	# print(resize)

	# screen_img = Image.new("P", (300, 400))
	# screen_img.paste(patch_im)
	screen_img.show()
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
