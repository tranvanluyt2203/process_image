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
characters_list = [chr(i) for i in range(ord("A"), ord("Z") + 1)]


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


def otsu_thresholding(image):
    # Tính histogram của ảnh
    hist = np.histogram(image, bins=256, range=(0, 256))[0]
    total_pixels = image.size
    sum_total = np.sum(image)
    sum_b = 0
    weight_b = 0
    max_variance = 0
    optimal_threshold = 0
    for threshold in range(256):
        weight_f = np.sum(hist[:threshold]) / total_pixels
        weight_b = 1 - weight_f
        if weight_f == 0 or weight_b == 0:
            continue
        sum_f = np.sum(np.arange(threshold) * hist[:threshold])
        mean_f = sum_f / (weight_f * total_pixels)
        mean_b = (sum_total - sum_f) / (weight_b * total_pixels)
        variance_between = weight_f * weight_b * ((mean_f - mean_b) ** 2)
        if variance_between > max_variance:
            max_variance = variance_between
            optimal_threshold = threshold
    return optimal_threshold


def detect_characters(img):
    image_gray = cv2.resize(img, (28, 28))
    threshold_value = otsu_thresholding(image_gray)
    binary_image = (image_gray > threshold_value).astype(
        np.uint8
    )  # > threshold = 1 else = 0
    binary_image[binary_image == 1] = 255
    image_text = cv2.resize(binary_image, (28, 28))
    result_pred = np.argmax(model.predict(image_text.reshape(-1, 28, 28, 1)), axis=-1)
    return characters_list[result_pred[0]]


def process_image(image_path):
    return detect_characters(np.array(Image.open(image_path)))
