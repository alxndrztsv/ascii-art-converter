from PIL import Image, ImageFont, ImageDraw
from colour import Color
import cv2
import numpy as np


# method changes pixels of the image to symbols
def pixels_to_ascii(image, symbols_len):
    image = image.convert('L')      # convert to greyscale B&W
    ascii_pic = ''
    for h in range(0, image.size[1]):
        for w in range(0, image.size[0]):
            pixel = image.getpixel((w, h))      # get pixel from the position (values from 0 to 256)
            ascii_pic += symbols[int(((symbols_len - 1) * pixel) / 255)]    # get the symbol from the list
        ascii_pic += '\n'   # go to a new line
    return ascii_pic


# this method will give the final product
def image_to_ascii(image, width_image, width_ascii, symbols, font, color_start, color_end, high_resolution):
    # check the way of calculation
    ascii_flag = True
    if not high_resolution and width_image <= 0:
        image = change_size(image, width_ascii, font, ascii_flag)  # get size of the image
    elif not high_resolution and width_image > 0:
        ascii_flag = False
        image = change_size(image, width_image, font, ascii_flag)

    ascii_image = pixels_to_ascii(image, len(symbols))  # transform pixels and get strings of ascii symbols
    image = draw_image(image, ascii_image, font, color_start, color_end)  # draw symbols to the image
    image.save('new_image.png')  # save the picture
    # txt_file = open('ascii.txt', 'w+')
    # txt_file.write(ascii_image)
    # txt_file.close()
    return image


# method changes changes the size
# the user sets the width
def change_size(image, width, font, ascii_flag):
    image_width = image.size[0]
    image_height = image.size[1]
    aspect_ratio = image_width / image_height

    if width <= 0:
        width = image_width

    symbol_width = font.getsize('&')[0]  # get the width in pixels (can be any letter) = 6
    symbol_height = font.getsize('&')[1]  # get the height in pixels (can be anything) = 11
    symbol_ratio = symbol_width / symbol_height

    if ascii_flag:
        image = image.resize((int(width / symbol_width), int(width / (aspect_ratio * symbol_height))))
    else:
        image = image.resize((width, int(width * symbol_ratio / aspect_ratio)))
    return image


def draw_image(image, ascii_image, font, color_start, color_end):
    bg_color = 'white'
    symbol_width = font.getsize('&')[0]  # get the width in pixels (can be any letter) = 6
    symbol_height = font.getsize('&')[1]  # get the height in pixels (can be anything) = 11
    new_image = Image.new('RGB', (int(image.size[0] * symbol_width),
                                  int(image.size[1] * symbol_height)), bg_color)
    draw = ImageDraw.Draw(new_image)
    ascii_list = ascii_image.split('\n')
    ascii_len = len(ascii_list)
    color_range = list(Color(color_start).range_to(Color(color_end), ascii_len))

    # print symbols to image
    left_padding = 0
    y = 0
    line_index = 0
    for line in ascii_list:
        color = color_range[line_index]
        line_index += 1
        draw.text((left_padding, y), line, color.hex, font=font)
        y += symbol_height
    return new_image


def video_to_ascii(video_width, ascii_width, high_resolution):
    file = 'video.mp4'
    cap = cv2.VideoCapture(file)

    # find the size of the future frames
    ret, frame = cap.read()
    frame_pil = Image.fromarray(frame)
    frame_test = image_to_ascii(frame_pil, video_width, ascii_width, small_symbols,
                                ImageFont.load_default(), 'black', 'black', high_resolution)
    frame_test_width = frame_test.size[0]
    image_test_height = frame_test.size[1]

    if video_width <= 0:
        video_width = frame_test_width

    fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
    # out = cv2.VideoWriter('output.avi', fourcc, 25, (video_width, video_width / aspect_ratio))
    out = cv2.VideoWriter('output.avi', fourcc, 25, (frame_test_width, image_test_height))
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            # frame_cv2 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)    # better picture but slow
            frame_pil = Image.fromarray(frame)
            frame_pil = image_to_ascii(frame_pil, video_width, ascii_width, small_symbols,
                                       ImageFont.load_default(), 'black', 'black', high_resolution)
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

    image_path = 'seoha.jpg'
    image = Image.open(image_path)
    width_image = 0
    width_ascii = 4608
    if width_image > 0:
        width_ascii = 0
    symbols = large_symbols
    font_type = None
    font_size = None
    if font_size is None:
        if font_type is None:
            font = ImageFont.load_default()
        else:
            font = ImageFont.load(font_type)
    else:
        font = ImageFont.truetype(font_type, font_size)
    color_start = 'black'
    color_end = 'black'
    high_resolution = False
    # image_to_ascii(image, width_image, width_ascii, symbols, font, color_start, color_end, high_resolution)

    video_width = 400
    ascii_width = 0
    video_to_ascii(video_width, ascii_width, high_resolution)
