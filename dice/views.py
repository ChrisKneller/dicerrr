from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader
from dice.forms import UploadForm
from chris_convert import dicify as chris_convert
import boto3
from lazysignup.decorators import allow_lazy_user
from django.views import View
from .models import DiceTypes
import os
from dice.models import DiceImage
import string
import random
import math
from datetime import datetime

# Create your views here.

def id_gen(size=8):
    chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(size))

@allow_lazy_user
def index(request):
    return redirect('upload')

@allow_lazy_user
def dindex(request):
    return HttpResponse(f"Hello, world. This is the dice index. Your temporary username is {request.user.username}")

def static_aws(url):
    session = boto3.session.Session(region_name='eu-west-2',aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID',''),aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY',''))
    s3client = session.client('s3')
    new_url = s3client.generate_presigned_url('get_object', Params = {'Bucket': 'diceart-media', 'Key': 'media/' + url}, ExpiresIn = 86400)
    return new_url

def model_form_upload(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            initial_obj = form.save(commit=False)
            initial_obj.save()
            uploaded_file_url = initial_obj.file.name
            uploaded_file_url = static_aws(uploaded_file_url)
            return render(request, 'dice/model_form_upload.html',
                {'uploaded_file_url': uploaded_file_url,
                'name': initial_obj.file.name})
    else:
        form = UploadForm()
    return render(request, 'dice/model_form_upload.html', {
        'form': form
    })

@allow_lazy_user
def create_lazyuser_then_redirect(request):
    return redirect('upload')

class AjaxUploadView(View):
    def get(self, request):
        if request.user.is_anonymous:
            return redirect('create_lazyuser')
        else:
            pass
        photos_list = []
        dice_list = DiceTypes.objects.all()
        return render(self.request, 'dice/ajax_upload.html',
            {'photos': photos_list,
            'dice_types': dice_list})

    def post(self, request):
        form = UploadForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = request.user
            photo.file.name = f'{id_gen(12)}.png'
            photo.save()
            uploaded_file_url = static_aws(photo.file.name)
            data = {'is_valid': True, 'name': photo.file.name,
                    'url': uploaded_file_url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)

def image_transform(request):
    # requires an input of just a filename e.g. cat.jpg
    # it will then run the function, extracting cat.jpg from the s3 storage box
    # and run the transformation on it
    if request.method == 'GET':
        return redirect('upload')
    elif request.method == 'POST':

        # if number of dice has been set, use it as the input
        try:
            num_dice = float(request.POST['number_of_dice'])
        except: # default to 10000 if not
            num_dice = 10000

        # run the transformation
        dice_dict = chris_convert(request.POST['img'], num_dice)

        image_id = id_gen()

        # update the model
        dice_model_object = DiceImage.objects.get_or_create(original_image=dice_dict["old_url"],
                                                            new_image=dice_dict["new_url"],
                                                            image_width=dice_dict["width_in_dice"],
                                                            image_height=dice_dict["height_in_dice"],
                                                            number_of_dice=dice_dict["number_of_dice"],
                                                            image_id = image_id,
                                                            uploaded_by = request.user)[0]
        dice_model_object.save()

        # get the accessible link for the new image so it can be shown on the page
        fname_raw = os.path.splitext(request.POST['img'])[0]
        new_url = static_aws(f'{fname_raw}-dice-{dice_dict["number_of_dice"]}.png')
        del dice_dict['new_url']
        dice_dict['new_url'] = new_url
        dice_dict['image_id'] = image_id

        return JsonResponse(dice_dict)

# share images by their custom identifier
def image_share(request, image_id): # from /share/<image_id>
    # TODO: VALIDATION
    # filter for the input URL
    print(f"{datetime.utcnow().isoformat()} share request started")
    dice_model_object = DiceImage.objects.filter(image_id=image_id)[0]
    print(f"{datetime.utcnow().isoformat()} share object loaded")
    dice_temp_url = static_aws((dice_model_object.new_image).split("/")[-1])
    print(f"{datetime.utcnow().isoformat()} share dice url generated")
    original_temp_url = static_aws((dice_model_object.original_image).split("/")[-1])
    print(f"{datetime.utcnow().isoformat()} share orig url generated")
    return render(request, 'dice/image_share.html', {
        'dice_image': dice_model_object,
        'dice_url': dice_temp_url,
        'original_url': original_temp_url
    })

# let a user view their uploads
def my_uploads(request, page=1):
    # dice_model_object = DiceImage.objects.filter(uploaded_by=request.user)[0]
    dice_model_objects = DiceImage.objects.filter(uploaded_by=request.user).order_by('-pk')
    number_of_pages = math.ceil(len(dice_model_objects)/5)
    dice_model_objects = dice_model_objects[page*5-5:page*5]
    dice_temp_urls = []
    original_temp_urls = []
    for dice_model_object in dice_model_objects:
        dice_temp_url = static_aws((dice_model_object.new_image).split("/")[-1])
        original_temp_url = static_aws((dice_model_object.original_image).split("/")[-1])
        dice_temp_urls.append(dice_temp_url)
        original_temp_urls.append(original_temp_url)
    return render(request, 'dice/my_uploads.html', {
        'dice_objects': dice_model_objects,
        'dice_urls': dice_temp_urls,
        'original_urls': original_temp_urls,
        'page': page,
        'number_of_pages': number_of_pages,
    })

# 404 page
def error404(request):
    template = loader.get_template('dice/404.html')
    context = {'message': 'Unfound'}
    return HttpResponse(content=template.render(context), content_type='text/html; charset=utf-8', status=404)