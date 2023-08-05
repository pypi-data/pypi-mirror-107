from PIL import ImageGrab


def save(name, extension):
    img = ImageGrab.grab()
    img.save(name, extension)
