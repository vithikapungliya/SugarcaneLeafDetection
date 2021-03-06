from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import numpy as np
from keras.models import load_model

from keras.preprocessing import image


# Create your views here.


model=load_model('models/Final_DenseNetSVM_Model.h5')


def index(request):
    context={'a':1}
    return render(request,'crop_index.html',context)

img_height, img_width=224,224

def predictImage(request):
    print (request)
    print (request.POST.dict())
    fileObj=request.FILES['filePath']
    fs=FileSystemStorage()
    filePathName=fs.save(fileObj.name,fileObj)
    filePathName=fs.url(filePathName)
    testimage='.'+filePathName
    img = image.load_img(testimage, target_size=(img_height, img_width))
    x = image.img_to_array(img)
    x=x/255
    x=x.reshape(img_height, img_width,3)
    x = np.expand_dims(x, axis=0)
    # with model_graph.as_default():
    #     with tf_session.as_default():
    predi=model.predict(x)
    print(predi)
    classes_x=np.argmax(predi)
    
    print(classes_x)
    classes=["Healthy","Red Rot", "Red Rust"]      
    MaxPosition=np.argmax(predi)  
    global prediction_label
    prediction_label=prediction_label=classes[MaxPosition]
    print(prediction_label)

    context={'filePathName':filePathName,'predictedLabel':prediction_label}
    return render(request,'crop_index.html',context) 



