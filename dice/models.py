from django.db import models
from django.contrib import admin
import random
import os
from django.core.validators import URLValidator
from django.contrib.auth.models import User
from io import BytesIO
from PIL import Image as Img
from PIL import ExifTags
from django.core.files import File
from datetime import datetime, timedelta

# Create your models here.

def user_directory_path(instance, filename):
    new_filename = f"{os.path.splitext(filename)[0]}-{random.randint(0,99999999)}.png"
    return new_filename

def random_day_in_the_past(number_of_days=365):
    random.seed=483293849283048329084209384932840923840320
    return datetime.now()-timedelta(days=int(random.random()*number_of_days))

class Upload(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, default=1)
    description = models.CharField(max_length=255, blank=True)
#    document = models.ImageField(upload_to=user_directory_path, width_field='image_width', height_field='image_height')
    file = models.ImageField(upload_to=user_directory_path, width_field='image_width', height_field='image_height')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    image_width = models.IntegerField()
    image_height = models.IntegerField()

    def save(self, *args, **kwargs):
        if self.file:
            pilImage = Img.open(BytesIO(self.file.read()))
            try:
                for orientation in ExifTags.TAGS.keys():
                    if ExifTags.TAGS[orientation] == 'Orientation':
                        break
                exif = dict(pilImage._getexif().items())

                if exif[orientation] == 3:
                    pilImage = pilImage.rotate(180, expand=True)
                elif exif[orientation] == 6:
                    pilImage = pilImage.rotate(270, expand=True)
                elif exif[orientation] == 8:
                    pilImage = pilImage.rotate(90, expand=True)
            except:
                print("No EXIF data")
            output = BytesIO()
            pilImage.save(output, format='PNG', quality=100)
            output.seek(0)
            self.file = File(output, self.file.name)

        return super(Upload, self).save(*args, **kwargs)

class DiceImage(models.Model):
    original_image = models.TextField (validators=[URLValidator()])
    new_image = models.TextField (validators=[URLValidator()])
    image_width = models.IntegerField() # in dice
    image_height = models.IntegerField() # in dice
    number_of_dice = models.IntegerField()
    image_id = models.TextField()
    uploaded_by = models.ForeignKey(User, on_delete=models.PROTECT, default=1)
    date_created = models.DateTimeField(default=datetime.now)

    # @property
    def construction_cost(self):
        # return an approximate charge for time for construction
        # based on number of dice and 10 seconds per dice
        rate_per_hour = 40 # in £
        construction_time_seconds = self.number_of_dice * 10
        construction_time_hours = construction_time_seconds / 60 / 60
        construction_cost = rate_per_hour * construction_time_hours
        return construction_cost

    def __str__(self):
        return os.path.basename(self.new_image)

class DiceTypes(models.Model):
    dice_size = models.IntegerField() # in mm^3
    dice_cost = models.IntegerField() # in pence

class ConstructionCost(models.Model):
    time_per_dice = models.IntegerField() # it takes ~10 seconds per dice
