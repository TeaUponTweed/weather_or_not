from PIL import Image
from inky import InkyWHAT

def inky_show(im):
    im = Image.open(im)
    im = im.transpose(Image.ROTATE_90)
    inky_display = InkyWHAT("black")
    inky_display.set_border(inky_display.WHITE)
    assert inky_display.WIDTH == 400
    assert inky_display.HEIGHT == 300
    inky_display.set_image(im)
    inky_display.show()


if __name__ == '__main__':
	main(sys.argv[1])
