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
    
    if not success:
        print("Cannot read video format")
    else:
        if os.name == 'nt':
            os.system('color')
            os.system('cls') # Reset color and clear screen
        else:
            os.system('clear')
        while success:
            try:
                expected_end_time = time.time() + 1 / fps

                new_image_data = pixels_to_ascii(
                    resize_image(image, width), ascii_string)
                pixel_count = len(new_image_data)

                ascii_image = '\n'.join([new_image_data[index:(index+width)]
                                    for index in range(0, pixel_count, width)])
                
                # Move cursor back to the beginning
                print('\033[%d;%dH' % (0, 0))
                
                # cursor usually flashes a lot in the edges while playing the video
                # keep it away from the current frame by putting a newline at the beginning
                sys.stdout.write('\n' + ascii_image) 

                if expected_end_time > time.time():
                    time.sleep(expected_end_time - time.time())

                success, image = vidcap.read()
                
            except KeyboardInterrupt: # allow exiting the video playback with Ctrl+C
                os.system('cls' if os.name == 'nt' else 'clear')
                print("\n" + "Exiting...")
                exit()


if __name__ == '__main__':
    if (len(sys.argv) > 1):
        path = sys.argv[1]
    else:
        path = input('Input path to video file: ')
        path = path.replace('"', '') # make paths with quotations compatible

    if (len(sys.argv) > 2):
        width = int(sys.argv[2])
    else:
        width = 64

    if (len(sys.argv) > 3):
        ascii_string = sys.argv[3]
    else:
        ascii_string = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "[::-1]

    main(path, width, ascii_string)
