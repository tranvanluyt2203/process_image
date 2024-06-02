# myapp/views.py
from django.shortcuts import render
from django.http import JsonResponse
from .forms import UploadImageForm
from keras.models import load_model
from keras.preprocessing import image
import os
import cv2
import numpy as np
from PIL import Image

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "static", "models", "model_detect_image.keras")
# Đọc mô hình từ file
model = load_model(MODEL_PATH)
encode = {0:'A',1:'B',2:'C',3:'D',4:'E',5:'F',6:'G',7:'H',8:'I',9:'J',10:'K',11:'L',12:'M',13:'N',14:'O',15:'P',16:'Q',17:'R',18:'S',19:'T',20:'U',21:'V',22:'W',23:'X', 24:'Y',25:'Z'}

def upload_image(request):
    result = None
    img_path = None
    if request.method == "POST":
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            img = form.cleaned_data["image"]
            img_path = os.path.join("media/images", img.name)
            img_full_path = os.path.join(BASE_DIR, img_path)
            with open(img_full_path, "wb") as f:
                for chunk in img.chunks():
                    f.write(chunk)
            # Xử lý hình ảnh và dự đoán
            prediction = process_image(img_full_path)
            result = prediction
    else:
        form = UploadImageForm()
    return render(
        request,
        "upload_image.html",
        {
            "form": form,
            "result": result,
            "url_image": img_path,
        },
    )


def process_image(image_path):
    image_ = Image.open(image_path)
    image_ = image_.convert("L")
    image_ = np.array(image_.resize((28, 28))).astype(np.float32).reshape(28, 28, 1)/255
    predict = model.predict(np.array([image_]))
    label = np.argmax(predict,axis = 1)
    
    return encode[label[0]]
