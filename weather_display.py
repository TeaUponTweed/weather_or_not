from PIL import Image, ImageFont, ImageDraw
# from scipy import signal
# from skimage.filters import threshold_sauvola
import fire
import imageio
import matplotlib.pyplot as plt
import numpy as np


def _load_gray(img):
    x = imageio.imread(img)[:,:,:3]
    x = np.linalg.norm(x, axis=2)/np.sqrt(3)
    return x


def make_template(img):
    x = _load_gray(img)
    xsub = x[350:400,475:600]
    plt.imshow(xsub)
    plt.show()
    np.savetxt('template.txt', np.round(xsub).astype(np.int), fmt='%u')


def _find_template_in_img(x, xsub, debug=False):
    m = np.mean(x)
    x = x - m
    s = np.std(x)
    x = x / s
    xsub = (xsub - m)/s
    m = np.mean(xsub)
    xsub = xsub - m
    x = x - m
    X = np.fft.fft2(x)
    # print(xsub.shape)
    xsub = xsub[:int(xsub.shape[0]//2*2),:int(xsub.shape[1]//2*2)]
    # print(xsub.shape)
    Xsub = np.fft.fft2(xsub, X.shape)
    # Xnorm = np.fft.fft2(np.ones(xsub.shape), X.shape)
    z = np.abs(np.fft.ifft2(np.conj(Xsub)*X))
    znorm = 1
    # znorm = np.abs(np.fft.ifft2(np.conj(Xsub)*Xnorm))
    # znorm[znorm == 0] = 1
    # z = z/znorm
    # z = z[int(xsub.shape[0]/2):int(-xsub.shape[0]/2)]


    # z = signal.correlate(x, xsub, mode = 'valid')
    # znorm = signal.correlate(np.abs(x), np.ones(xsub.shape), mode = 'valid')
    # z = z / znorm
    if debug:
        print('xsub')
        plt.imshow(xsub)
        plt.show()

        print('z')
        plt.imshow(z)
        plt.show()

        # print('znorm')
        # plt.imshow(znorm)
        # plt.show()

    if debug:
        print('z')
        plt.imshow(z)
        plt.show()

    row, col = np.unravel_index(z.argmax(), z.shape)

    return int(np.round(row)), int(np.round(col))


def make_weather_bw(img, template, debug=False):
    # find anchor in image
    im = _load_gray(img)
    t = np.loadtxt(template)
    row, col = _find_template_in_img(im, t, debug=debug)
    if debug:
        plt.imshow(im, cmap='gray', vmin=0, vmax=255)
        plt.plot([col],[row], color='r',marker='x')
        plt.show()

    # extract patches from image relative to anchor
    patch_1 = [-170, -295, 190, 225]
    patch_2 = [180, -277, 110, 225]
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
    # darken image so that small text is more clear
    patch[patch < 220] = patch[patch < 220] - 150
    patch = np.maximum(patch, 0)
    if np.any(np.isnan(patch)):
        print('NaN in image')
        patch = 255*np.ones(patch.size)

    # resize image to fill display  
    aspect_ratio = patch.shape[1]/patch.shape[0]
    if 400*aspect_ratio <= 300:
        new_size = (400, min(int(round(400*aspect_ratio)),300))
    else:
        new_size = (min(int(round(300/aspect_ratio)),400), 300)
    new_size = (new_size[1], new_size[0])
    patch_im = Image.fromarray(np.uint8(patch))
    patch_im = patch_im.resize(new_size)
    screen_img = Image.new("P", (300, 400))
    screen_img.paste(patch_im)
    # convert image to black/white
    pal_img = Image.new("P", (1, 1))
    pal_img.putpalette((255, 255, 255, 0, 0, 0) + (0, 0, 0) * 253)
    screen_img = screen_img.convert("RGB").quantize(palette=pal_img).transpose(Image.ROTATE_90)
    # print(screen_img.width)
    # display or output image
    screen_img.save("latest.png")

def inky_show(im):
    im = Image.open(im)
    from inky import InkyWHAT
    inky_display = InkyWHAT("black")
    inky_display.set_border(inky_display.WHITE)
    assert inky_display.WIDTH == 400
    assert inky_display.HEIGHT == 300
    # assert inky_display.WIDTH == im.WIDTH
    # assert inky_display.HEIGHT == im.HEIGHT
    inky_display.set_image(im)
    from multiprocessing import Process
    for _ in range(3):
        p1 = Process(target=lambda: inky_display.show(), name='Show Inky')
        p1.start()
        p1.join(timeout=15)
        if p1.exitcode is not None:
            break
    else:
        print('Failed to show on inky')


if __name__ == '__main__':
    fire.Fire()
