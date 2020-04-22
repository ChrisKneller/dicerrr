from PIL import Image # for image manipulation
from math import sqrt # for dimension calculation
import requests # for accessing web
import io # for dealing with image formatting (read/write)
from aws_link_gen import transform_url
from dice_gen import s3
from sys import argv
import os

# Set whether we are using local files or not (local files is for initial testing)
local = False

# Set the size of the dice
dice_size = 10

# Set whether you want the image to show a frame and set its thickness (10 = 1 dice; 30 = 3 dice)
framed = True
frame_thickness = 20

# Set the approximate number of dice to use
set_dice_to_use = True
if set_dice_to_use:
    dice_to_use = 10000
else:
    scale = 2

# Set details about where to find the images
directory = "https://s3.eu-west-2.amazonaws.com/diceart-media/"
image_to_convert = "Koala-27432481"
image_extension = ".jpg"

def dicify(image_to_convert, dice_to_use):

    dice_to_use = int(dice_to_use)

    # If the input URL contains an extension separate that from the filename
    if "." in image_to_convert:
        image_to_convert, image_extension = os.path.splitext(image_to_convert)

    # Initiliase list
    dice_1 = dice_2 = dice_3 = dice_4 = dice_5 = dice_6 = None
    dice_list = [dice_1, dice_2, dice_3, dice_4, dice_5, dice_6]

    if not local:
        # Open images from URL (i.e. Amazon S3)
        # # Image to convert
        presigned_url = transform_url(image_to_convert + image_extension)
        response = requests.get(presigned_url)
        img = Image.open(io.BytesIO(response.content))
        # # Individual dice images
        for dice in range(len(dice_list)):
            response = requests.get(f"{directory}static/{dice_size}x{dice_size}-dice-{str(dice+1)}-border.png")
            dice_list[dice] = Image.open(io.BytesIO(response.content))
    else:
        # Open the images if they are stored locally
        img = Image.open(image_to_convert + image_extension)
        for dice in range(len(dice_list)):
            dice_list[dice] = Image.open(f"{dice_size}x{dice_size}-dice-{str(dice+1)}.png")

    # Calculations based on dice_to_use to determine scale factor
    width, height = img.size
    if set_dice_to_use:
        original_number_of_dice = width * height / 100 # /100 because each 10 pixels is 1 die. 10x10 = 100
        scale = sqrt(dice_to_use / original_number_of_dice)

    print(f'Width: {width}; height: {height}')

    # New dimensions
    width = int(round(img.size[0]*scale,-1))
    height = int(round(img.size[1]*scale,-1))

    # Scale image by factor of {scale} above straight away (determined by dice_to_use)
    img = img.resize((width,height),Image.NEAREST)

    # Get the dimensions of the scaled up image
    width, height = img.size
    width_in_dice = int(width / 10)
    height_in_dice = int(height / 10)
    number_of_dice_used = int(width * height / 100)

    print(f'Width: {width}; height: {height}')

    # Set new dimensions
    new_width = width//dice_size
    new_height = height//dice_size

    # Resize smoothly down to chosen dice_size pixels
    imgSmall = img.resize((new_width,new_height),resample=Image.BILINEAR)

    # Scale back up using NEAREST to original size
    result = imgSmall.resize(img.size,Image.NEAREST) # .convert('LA') this would convert to greyscale

    # Create a new blank image with same dimension in greyscale
    result_greyscale = Image.new('L', (width, height))

    # Loop over colour pixels in pixelated image, convert them to gresycale add them into the new image
    # This is slightly better than .convert('LA') as it gives each pixel a greyscale value (0-255)
    # instead of (L,255) where L is luminosity and only really ranges between 6 and 21
    for x in range (0, width):
        for y in range(0, height):
            try:
                r, g, b = result.getpixel((x, y))
            except:
                r = result.getpixel((x, y))[0]
                g = result.getpixel((x, y))[1]
                b = result.getpixel((x, y))[2]
            value = r * 299.0/1000 + g * 587.0/1000 + b * 114.0/1000
            value = int(value)
            result_greyscale.putpixel((x, y), value)

    # These are just to test that everything makes sense. max_dice_value should be maximum 6 if everything works
    max_dice_value = 0
    count_1 = 0
    count_2 = 0
    count_3 = 0
    count_4 = 0
    count_5 = 0
    count_6 = 0

    # Create a new blank image with same dimension for the dice image
    dice_image = Image.new('L', (width, height))

    # Loop over each pixel and assign a dice face to it, then add that dice in the appropriate place
    # in the new dice image we are creating
    for x in range(0,width-1,dice_size):
        for y in range(0,height-1,dice_size):
            p_details = result_greyscale.getpixel((x,y))
            dice_rep = int(p_details/42.67) + 1 # this ensures every value 0-255 gets assigned in the range 1-6
            if dice_rep == 1: # dice_rep = 1 actually represents the dice face 6; all are inversed because 0 = black
                count_1 += 1
                dice_image.paste(dice_list[5].copy(),(x,y))
            if dice_rep == 2:
                count_2 += 1
                dice_image.paste(dice_list[4].copy(),(x,y))
            if dice_rep == 3:
                count_3 += 1
                dice_image.paste(dice_list[3].copy(),(x,y))
            if dice_rep == 4:
                count_4 += 1
                dice_image.paste(dice_list[2].copy(),(x,y))
            if dice_rep == 5:
                count_5 += 1
                dice_image.paste(dice_list[1].copy(),(x,y))
            if dice_rep == 6:
                count_6 += 1
                dice_image.paste(dice_list[0].copy(),(x,y))
            if dice_rep > max_dice_value:
                max_dice_value = dice_rep

    # print(f'Max dice = {max_dice_value}')
    print(f'Counts: {count_1},{count_2},{count_3},{count_4},{count_5},{count_6}')

    # If the number of dice to use hasn't been set, add "reg" to the name
    if not set_dice_to_use:
        dice_to_use = "reg"

    # If framed set to True, create and save a framed image
    if framed:
        framed_dice_image = Image.new('L', (width + frame_thickness*2, height + frame_thickness*2))
        framed_dice_image.paste(dice_image, (frame_thickness,frame_thickness))

    if not local:
        # Convert PIL image to format suitable for s3 upload; then upload
        # Only saving the dicified image for now
        out_image = io.BytesIO()
        dice_image.save(out_image, format='png')
        out_image.seek(0)
        s3.Bucket('diceart-media').put_object(Key=f"media/{image_to_convert}-dice-{number_of_dice_used}.png", Body=out_image, ContentType = 'image/png')
    else:
        # Save the pixelated colour image, the pixelated greyscale image and the dice image locally
        result.save(f"{image_to_convert}-pixelated.png")
        result_greyscale.save(f"{image_to_convert}-grey-pixelated.png")
        dice_image.save(f"{image_to_convert}-{dice_to_use}-dice.png")
        framed_dice_image.save(f"{image_to_convert}-{dice_to_use}-dice-framed.png")

    new_url = f"{directory}media/{image_to_convert}-dice-{number_of_dice_used}.png"
    old_url = f"{directory}media/{image_to_convert}{image_extension}"

    return_data = {'old_url': old_url,
                    'new_url': new_url,
                    'width_in_dice': width_in_dice,
                    'height_in_dice': height_in_dice,
                    'number_of_dice': number_of_dice_used
                    }

    return return_data


if __name__ == '__main__':
    dicify(argv[1], argv[2])