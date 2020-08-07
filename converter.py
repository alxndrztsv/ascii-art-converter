from PIL import Image, ImageFont, ImageDraw
import cv2
import numpy as np


def get_pixel_color(image, width, height):
    return image.getpixel((width, height))


# method changes pixels of the image to symbols
def pixels_to_ascii(image, symbols):
    # convert to greyscale B&W
    grey_image = image.convert('L')
    ascii_pic = ''
    for h in range(0, grey_image.size[1]):
        for w in range(0, grey_image.size[0]):
            # get pixel from the position (values from 0 to 256)
            pixel = grey_image.getpixel((w, h))
            # get the symbol from the list
            ascii_pic += symbols[int(((len(symbols) - 1) * pixel) / 255)]
        ascii_pic += '\n'   # go to a new line
    return ascii_pic.strip()


# this method will give the final product
def image_to_ascii(image, width, symbols, font, bg_color):
    # get the width in pixels (can be any letter) = 6
    symbol_width = font.getsize('&')[0]
    # get the height in pixels (can be anything) = 11
    symbol_height = font.getsize('&')[1]
    # check the way of calculation
    image = change_size(image, width, symbol_width, symbol_height)
    # transform pixels and get strings of ascii symbols
    ascii_image = pixels_to_ascii(image, symbols)
    # draw symbols to the image
    image = draw_image(image, ascii_image, symbol_width, symbol_height, bg_color)
    # save the picture
    image.save('new_image.jpg')

    # # optional: can save symbols into the txt doc # #
    # txt_file = open('ascii.txt', 'w+')
    # txt_file.write(ascii_image)
    # txt_file.close()

    return image


# method changes changes the size
# the user sets the width
def change_size(image, width, symbol_width, symbol_height):
    image_width = image.size[0]
    image_height = image.size[1]
    aspect_ratio = image_width / image_height
    # resize the image taking into account aspect ratio
    image = image.resize((int(width / symbol_width), int(width / (aspect_ratio * symbol_height))))
    return image


def draw_image(image, ascii_image, symbol_width, symbol_height, bg_color):
    new_image = Image.new('RGB', (int(image.size[0] * symbol_width),
                                  int(image.size[1] * symbol_height)), bg_color)
    d = ImageDraw.Draw(new_image)
    ascii_list = ascii_image.split('\n')

    # # optional: lines can be painted in different colors # #
    # ascii_len = len(ascii_list)
    # color_range = list(Color(color_start).range_to(Color(color_end), ascii_len))
    # line_index = 0

    y = 0
    # go through each line of symbols
    for line_index in range(len(ascii_list)):
        left_padding = 0
        # go through each character in a line
        for char_index in range(len(ascii_list[line_index])):

            # color = color_range[line_index]

            color = get_pixel_color(image, char_index, line_index)

            # line_index += 1
            # d.text((left_padding, y), line, color.hex, font=font)

            d.text((left_padding, y), ascii_list[line_index][char_index], fill=color, font=font)
            left_padding += symbol_width
        y += symbol_height
    return new_image


def video_to_ascii(file, symbols, font, bg_color):
    cap = cv2.VideoCapture(file)

    # find the size of the future frames
    ret, frame = cap.read()
    frame_pil = Image.fromarray(frame)
    width = frame_pil.size[0]
    # width can be change for better visualization 2560, 3840 shows a good picture
    frame_test = image_to_ascii(frame_pil, width, symbols, font, bg_color)
    frame_test_width = frame_test.size[0]
    image_test_height = frame_test.size[1]

    fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
    # save to the file
    out = cv2.VideoWriter('output.avi', fourcc, 25, (frame_test_width, image_test_height))
    # go through each frame
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            # for a better picture
            # frame_cv2 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # open the frame with PIL passing bytes
            frame_pil = Image.fromarray(frame)
            # converting the frame to ascii
            frame_pil = image_to_ascii(frame_pil, frame_test_width, symbols, font, bg_color)
            # converting image from PIL to opencv to add the frame to the video file
            out.write(np.asarray(frame_pil))
            if cv2.waitKey(1) and 0xFF == ord('q'):
                break
        else:
            break
    cap.release()
    out.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    small_symbols = '@%#*+=-:.'  # from darkest to lightest
    medium_symbols = 'B8&WM#YXQ0{}[]()I1i!pao;:,.'  # from darkest to lightest
    large_symbols = '$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`\'. '  # from darkest to lightest

    # choose your video to convert
    video_path = 'video.mp4'
    # choose your image to convert
    image_path = 'image.jpg'

    image = Image.open(image_path)
    image_width = image.size[0]
    symbols = large_symbols
    font = ImageFont.load_default()
    # font can be changed here
    # font = ImageFont.truetype('arialbd.ttf', 8)
    bg_color = (75, 75, 75)

    try:
        image_to_ascii(image, image_width, symbols, font, bg_color)
        # video_to_ascii(video_path, symbols, font, bg_color)
    except:
        Exception('Something went wrong...')