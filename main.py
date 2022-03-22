import cv2
import os
import sys
import time


def resize_image(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image

    if width is None:
        r = height / float(h) * 2
        dim = (int(w * r), height)

    else:
        r = width / float(w) * 0.5
        dim = (width, int(h * r))

    resized = cv2.resize(image, dim, interpolation=inter)
    return resized


def pixels_to_ascii(image, ascii_string):
    rows, cols, _ = image.shape

    characters = ''

    for x in range(rows):
        for y in range(cols):
            r, g, b = image[x, y]

            brightness = ((0.21 * r) + (0.72 * g) + (0.07 * b)) / 255

            characters += ascii_string[int(len(ascii_string) * brightness)]

    return(characters)


def main(path, width, ascii_string):
    vidcap = cv2.VideoCapture(path)
    fps = vidcap.get(cv2.CAP_PROP_FPS)
    success, image = vidcap.read()

    while success:
        expected_end_time = time.time() + 1 / fps

        new_image_data = pixels_to_ascii(
            resize_image(image, width), ascii_string)
        pixel_count = len(new_image_data)

        ascii_image = '\n'.join([new_image_data[index:(index+width)]
                                 for index in range(0, pixel_count, width)])

        os.system('cls' if os.name == 'nt' else 'clear')
        print(ascii_image)

        if expected_end_time > time.time():
            time.sleep(expected_end_time - time.time())

        success, image = vidcap.read()


if __name__ == '__main__':
    if (len(sys.argv) > 1):
        path = sys.argv[1]
    else:
        path = input('Input path to video file')

    if (len(sys.argv) > 2):
        width = sys.argv[2]
    else:
        width = 64

    if (len(sys.argv) > 3):
        ascii_string = sys.argv[3]
    else:
        ascii_string = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "[::-1]

    main(path, width, ascii_string)
