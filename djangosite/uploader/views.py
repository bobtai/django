import os

import tensorflow as tf
from keras.models import load_model
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from uploader.models import UploadForm, Upload

mnist_model_Path = os.path.join(settings.MEDIA_ROOT, "models/MnistCNNModel.h5")
model = load_model(mnist_model_Path)
graph = tf.get_default_graph()

# Create your views here.
def uploader(request):
    if request.method == "POST":
        img = UploadForm(request.POST, request.FILES)       
        if img.is_valid():
            pic = request.FILES['pic']
            img_obj = Upload(pic=pic)
            img_obj.save()  

            img_Path = os.path.join(settings.MEDIA_ROOT, "images/" + pic.name)
            normalized_image = image_normalize(img_Path)
            
            with graph.as_default():
                prediction = model.predict_classes(normalized_image)

            img_obj.description = "此圖經 Mnist Model 辨識為 " + str(prediction[0])
            img_obj.save()

            return HttpResponseRedirect(reverse('uploader'))
    else:
        img = UploadForm()
    images = Upload.objects.all()
    return render(request, 'upload.html', {'form':img,'images':images})

def image_normalize(imagepath):
    filename_queue = tf.train.string_input_producer([imagepath])
    reader = tf.WholeFileReader()
    key, value = reader.read(filename_queue)
    myimg = tf.image.decode_png(value, channels=1)
    crop_myimg = tf.image.resize_image_with_crop_or_pad(myimg, 140, 140)
    resize_myimg = tf.image.resize_images(crop_myimg, [28, 28])
    
    with tf.Session() as sess:
        init = tf.global_variables_initializer()
        sess.run(init)
    
        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(coord=coord)
    
        image = resize_myimg.eval().reshape(1, 28, 28, 1)
        normalized_image = abs(255 - image).astype('float32') / 255

        coord.request_stop()
        coord.join(threads)
    
    return normalized_image