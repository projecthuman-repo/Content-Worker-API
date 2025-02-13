import cv2
from PIL import Image
from fastapi import APIRouter, File, UploadFile
#from nudepy import Nude
import requests
import aiohttp
import numpy as np
import tensorflow as tf
import keras

MODEL_PATH = 'Content-Worker-API/image_model/nsfw_model/merged_trained_nsfw_mobilenet_224x244_30.h5'

router = APIRouter()

@router.post("/image_moderation")
def classify_image(image_path: str):
    """
    This method is taking image path and performing prediction with Keras or torch model
    And return a tuple containing predicted class and model predictions"""
    
    class_labels = ['normal','nude','voilance']
    
    id2label = {i: label for i, label in enumerate(class_labels)}
    img_height, img_width = 224, 224 # Define image size
    img = Image.open(image_path)
    # Resize the image to the required input size
    img = img.resize((img_width, img_height))
    # Convert the image to a numpy array
    img_array = np.array(img)
    # Normalize the image (if your model expects normalized inputs)
    img_array = img_array / 255.0
    # Add batch dimension
    img_array = np.expand_dims(img_array, axis=0)



    model = keras.models.load_model(MODEL_PATH, compile=False)

    predictions = model.predict(img_array)
    # Get the predicted class index
    predicted_class_idx = np.argmax(predictions, axis=1)[0]
    # Get the predicted class label
    Predicted_class = id2label[predicted_class_idx]
    # Get the prediction percentages for all classes
    prediction_percentages = tf.nn.softmax(predictions).numpy()[0] * 100
    formatted_predictions = {class_labels[i]: f"{percentage:.2f}%" for i, percentage in enumerate(prediction_percentages)}

    return {
    "status": "success",
    "message": "File processed successfully.",
    "Result": {"Predicted_class" : Predicted_class, "formatted_predictions" : formatted_predictions}
  }
