from PIL import Image # for image manipulation
import boto3 # for saving to AWS S3
import io # for conversion of image into suitable format for S3
import os

save_to_s3 = True
scale = 9
border = False

# This file is used to generate

# Set AWS S3 info to save to bucket
AWS_ACCESS_KEY_ID=os.environ.get('AWS_ACCESS_KEY_ID','')
AWS_SECRET_ACCESS_KEY=os.environ.get('AWS_SECRET_ACCESS_KEY','')
session = boto3.session.Session(region_name='eu-west-2',
                                aws_access_key_id=AWS_ACCESS_KEY_ID,
                                aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
s3 = session.resource('s3')
s3client = session.client('s3')

def generate_dice(save_to_s3=True, scale=9, border=False):

    # Initialise new dice images as white squares with scale as dimension
    six = Image.new('L', (scale, scale), 255)
    five = Image.new('L', (scale, scale), 255)
    four = Image.new('L', (scale, scale), 255)
    three = Image.new('L', (scale, scale), 255)
    two = Image.new('L', (scale, scale), 255)
    one = Image.new('L', (scale, scale), 255)

    dice_list = [one, two, three, four, five, six]

    # Loop over every pixel and put dots where appropriate
    # This is terribly ineffecient but was written a long time ago
    for x in range(0,scale):
        for y in range(0,scale):
            if scale == 9: # dot placements for 9x9 faces
                if x == 2 and y == 2: # upper left dot
                    six.putpixel((x,y),0) # 0 is the greyscale value for black
                    five.putpixel((x,y),0)
                    four.putpixel((x,y),0)
                if x == 2 and y == 4: # middle left dot
                    six.putpixel((x,y),0)
                if x == 2 and y == 6: # lower left dot
                    six.putpixel((x,y),0)
                    five.putpixel((x,y),0)
                    four.putpixel((x,y),0)
                    three.putpixel((x,y),0)
                    two.putpixel((x,y),0)
                if x == 4 and y == 4: # centre dot
                    five.putpixel((x,y),0)
                    three.putpixel((x,y),0)
                    one.putpixel((x,y),0)
                if x == 6 and y == 2: # upper right dot
                    six.putpixel((x,y),0)
                    five.putpixel((x,y),0)
                    four.putpixel((x,y),0)
                    three.putpixel((x,y),0)
                    two.putpixel((x,y),0)
                if x == 6 and y == 4: # middle right dot
                    six.putpixel((x,y),0)
                if x == 6 and y == 6: # lower right dot
                    six.putpixel((x,y),0)
                    five.putpixel((x,y),0)
                    four.putpixel((x,y),0)
            if scale == 10: # dot placements for 10x10 faces
                if (x == 1 or x == 2) and (y == 1 or y == 2): # upper left dot
                    six.putpixel((x,y),0)
                    five.putpixel((x,y),0)
                    four.putpixel((x,y),0)
                if (x == 1 or x == 2) and (y == 4 or y == 5): # middle left dot
                    six.putpixel((x,y),0)
                if (x == 1 or x == 2) and (y == 7 or y == 8): # lower left dot
                    six.putpixel((x,y),0)
                    five.putpixel((x,y),0)
                    four.putpixel((x,y),0)
                    three.putpixel((x,y),0)
                    two.putpixel((x,y),0)
                if (x == 4 or x == 5) and (y == 4 or y == 5): # centre dot
                    five.putpixel((x,y),0)
                    three.putpixel((x,y),0)
                    one.putpixel((x,y),0)
                if (x == 7 or x == 8) and (y == 1 or y == 2): # upper right dot
                    six.putpixel((x,y),0)
                    five.putpixel((x,y),0)
                    four.putpixel((x,y),0)
                    three.putpixel((x,y),0)
                    two.putpixel((x,y),0)
                if (x == 7 or x == 8) and (y == 4 or y == 5): # middle right dot
                    six.putpixel((x,y),0)
                if (x == 7 or x == 8) and (y == 7 or y == 8): # lower right dot
                    six.putpixel((x,y),0)
                    five.putpixel((x,y),0)
                    four.putpixel((x,y),0)
    return dice_list

def save_dice(save_to_s3=True, ):
    dice_list = generate_dice()
    if save_to_s3:
        # Convert each PIL Image into an image format suitable for S3 and then upload
        for dice in range(len(dice_list)):
            out_image = io.BytesIO()
            dice_list[dice].save(out_image, format='png')
            out_image.seek(0)
            s3.Bucket('diceart-media').put_object(Key=f"static/{scale}x{scale}-dice-{str(dice+1)}.png", Body=out_image, ContentType = 'image/png')
    else:
        # Save each dice to current directory
        for dice in range(len(dice_list)):
            dice_list[dice].save(f"{scale}x{scale}-dice-{str(dice+1)}.png")

if __name__ == '__main__':
    save_dice()