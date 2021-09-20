from PIL import Image, ImageDraw, ImageFont
import numpy
import base64
from io import BytesIO

# image (PNG, JPG) to base64 conversion (string), learn about base64 on wikipedia https://en.wikipedia.org/wiki/Base64
def image_base64(img, img_type):
    with BytesIO() as buffer:
        img.save(buffer, img_type) #this saves the image as something different/converts it into binary for the data
        return base64.b64encode(buffer.getvalue()).decode() #after dot is a function
# formatter preps base64 string for inclusion, ie <img src=[this return value] ... />
def image_formatter(img, img_type):
    return "data:image/" + img_type + ";base64," + image_base64(img, img_type)
# color_data prepares a series of images for data analysis

def image_data(path="static/", img_list=None):  # path of static images is defaulted
    if img_list is None:  # color_dict is defined with defaults
        img_list = [
            {'source': "Romolo Tavani ", 'label': "Drowning Hand", 'file': "rip.jpg"}, # this is one dictionary where the source is the word and the "smiley" is the definition
        ]
    # gather analysis data and meta data for each image, adding attributes to each row in table
    for img_dict in img_list:
        img_dict['path'] = '/' + path  # path for HTML access (frontend)
        file = path + img_dict['file']  # file with path for local access (backend)
        # Python Image Library operations
        img_reference = Image.open(file)  # PIL: this is opeening the image like if we did image.open(static/smiley.jpg) adn this creates an instance of the image. image.open() is a function that loads the image and creates an image pbject that can be modified with the .save: the image object we recieve using image.open can later be used to resize, crop, or more the image
        draw = ImageDraw.Draw(img_reference)
        #myFont = ImageFont.truetype('E:/PythonPillow/Fonts/FreeMono.ttf', 30)
        draw.text((75, 20), "APCSP IS COOL", fill=(255, 0, 0))
        img_data = img_reference.getdata()  # Reference https://www.geeksforgeeks.org/python-pil-image-getdata/ this gets the binary from the RGB without meta data :  Image.open() reads the image and gets all relevant info from the image.
        img_dict['format'] = img_reference.format #jpeg vs png (file format)
        img_dict['mode'] = img_reference.mode #pixel format s o RGB vs RGBA
        img_dict['size'] = img_reference.size #height and width of the image
        # Conversion of original Image to Base64, a string format that serves HTML nicely
        img_dict['base64'] = image_formatter(img_reference, img_dict['format'])
        # Numpy is used to allow easy access to data of image, python list
        img_dict['data'] = numpy.array(img_data)
        img_dict['hex_array'] = []
        img_dict['binary_array'] = []
        # 'data' is a list of RGB data, the list is traversed and hex and binary lists are calculated and formatted
        for pixel in img_dict['data']:
            # hexadecimal conversions
            hex_value = hex(pixel[0])[-2:] + hex(pixel[1])[-2:] + hex(pixel[2])[-2:]
            hex_value = hex_value.replace("x", "0")
            img_dict['hex_array'].append("#" + hex_value)
            # binary conversions
            bin_value = bin(pixel[0])[2:].zfill(8) + " " + bin(pixel[1])[2:].zfill(8) + " " + bin(pixel[2])[2:].zfill(8)
            img_dict['binary_array'].append(bin_value)
        # create gray scale of image, ref: https://www.geeksforgeeks.org/convert-a-numpy-array-to-an-image/
        img_dict['gray_data'] = []
        for pixel in img_dict['data']:
            average = (pixel[0] + pixel[1] + pixel[2]) // 3
            if len(pixel) > 3:
                img_dict['gray_data'].append((average, average, average, pixel[3])) # append means to add it like when you do "" + something to create a string
            else:
                img_dict['gray_data'].append((average, average, average))
        img_reference.putdata(img_dict['gray_data'])
        img_dict['base64_GRAY'] = image_formatter(img_reference, img_dict['format'])
        draw = ImageDraw.Draw(img_reference)
        draw.text((0, 0), "Size is 600 X 600")  # draw in image
    return img_list  # list is returned with all the attributes for each image dictionary
# run this as standalone tester to see data printed in terminal


if __name__ == "__main__":
    local_path = "static/"
    img_test = [
        {'source': "iconsdb.com", 'label': "Blue square", 'file': "rip.jpg"},
    ]
    items = image_data(local_path, img_test)  # path of local run
    for row in items:
        # print some details about the image so you can validate that it looks like it is working
        # meta data
        print("---- meta data -----")
        print(row['size'])
        print("----  render and write in image  -----")
        filename = local_path + row['file']
        image_ref = Image.open(filename)
        draw = ImageDraw.Draw(image_ref)
        draw.text((0, 0), "Size is {0} X {1}".format(*row['size']))  # draw in image
        image_ref.show()
print()
