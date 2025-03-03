from transformers import VideoMAEImageProcessor, VideoMAEForVideoClassification
import pytorchvideo.data
import torchvision.transforms as T
import torch
import numpy as np
from pytorchvideo.transforms import (
    ApplyTransformToKey,
    Normalize,
    UniformTemporalSubsample,
)

from torchvision.transforms import (
    Compose,
    Lambda,
    Resize
)
import random
from torchvision.io import read_video
import cv2
import os
import requests
#device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
device = torch.device("cpu")
VIDEO_MODEL_PATH = os.getenv("VIDEO_MODEL_PATH")
RESULT_API_URL = os.getenv("RESULT_API_URL", "http://localhost:8080/result")


image_processor = VideoMAEImageProcessor.from_pretrained(VIDEO_MODEL_PATH)
mean = image_processor.image_mean
std = image_processor.image_std

class_labels = ['normal','nude','voilance']

label2id = {label: i for i, label in enumerate(class_labels)}
id2label = {i: label for i, label in enumerate(class_labels)}


if "shortest_edge" in image_processor.size:
    height = width = image_processor.size["shortest_edge"]
else:
    height = image_processor.size["height"]
    width = image_processor.size["width"]
resize_to = (height, width)


#model_ckpt =  "MCG-NJU/videomae-base"
batch_size = 12 # batch size for training and evaluation

def load_video_opencv(video_path):
    cap = cv2.VideoCapture(video_path)
    frames = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
        frames.append(frame)
    cap.release()
    return np.array(frames)

def preprocess_video(video_path, num_frames_to_sample = 16):
    
    video = load_video_opencv(video_path)  # Shape: [T, H, W, C]
    print(f"Video shape: {video.shape}, dtype: {video.dtype}")
    video = torch.tensor(video, dtype=torch.float32)
    print(f"Video shape: {video.shape}, dtype: {video.dtype}")

    # *** KEY CHANGE: Handle number of frames BEFORE transforms ***
    num_frames = video.shape[0]
    if num_frames > num_frames_to_sample:
        # Subsample if more frames
        indices = torch.linspace(0, num_frames - 1, num_frames_to_sample).long()
        video = video[indices]
    elif num_frames < num_frames_to_sample:
        # Pad if less frames (more complex, but necessary for consistent input)
        padding = torch.zeros((num_frames_to_sample - num_frames, video.shape[1], video.shape[2], video.shape[3]), dtype=video.dtype, device=video.device)
        video = torch.cat([video, padding], dim=0)

    
    # Convert to float and normalize
    
    # Create validation transform
    val_transform = Compose([
        ApplyTransformToKey(
            key="video",
            transform=Compose([
                UniformTemporalSubsample(num_frames_to_sample),
                Lambda(lambda x: x.permute(3, 0, 1, 2)),  # [T, H, W, C] -> [C, T, H, W]
                Lambda(lambda x: x / 255.0),
                Normalize(mean, std),
                Resize(resize_to),
            ])
        )
    ])

    # Apply transforms
    sample = {'video': video}
    transformed = val_transform(sample)
    processed_video = transformed['video']  # Should be [C, T, H, W]
    
    print(f"Processed video shape: {processed_video.shape}")  # Debug
    return processed_video

async def predict_video(video_path):
    # Preprocess video
    processed_video = preprocess_video(video_path).to(device)
    perumuted_sample_test_video = processed_video.permute(1, 0, 2, 3)
    # Add batch dimension and verify final shape
    inputs = {
        "pixel_values": perumuted_sample_test_video.unsqueeze(0)
    }

    print(f"Model input shape: {inputs['pixel_values'].shape}")  # Should be [1, C, T, H, W]
    inputs = {k: v.to(device) for k, v in inputs.items()}
    model = VideoMAEForVideoClassification.from_pretrained(
    VIDEO_MODEL_PATH,
    label2id=label2id,
    id2label=id2label)
    num_frames_to_sample = model.config.num_frames
    sample_rate = 4
    fps = 30
    clip_duration = num_frames_to_sample * sample_rate / fps

    model = model.to(device)
    print("Final Input shape", inputs.keys())
    with torch.no_grad():
        outputs = model(**inputs)
    
    # Get probabilities
    probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
    probs = probabilities.squeeze().cpu().numpy()
    Predicted_class = model.config.id2label[probs.argmax()]
    
    print("\nPredicted class:", Predicted_class)
    print("Class probabilities:")
    formatted_predictions = {}
    for i, prob in enumerate(probs):
        print(f"- {model.config.id2label[i]}: {prob*100:.2f}%")
        formatted_predictions = {class_labels[i]: f"{prob*100:.2f}%"}

    result_payload = {
        "documentId": "some-unique-id",  # You need to generate a unique ID
        "status": "success",
        "message": "File processed successfully.",
        "Result": {
            "Predicted_class": Predicted_class,
            "outcome": formatted_predictions
        }
    }

    # Send the result to localhost:8080/result
    try:
        response = requests.post(RESULT_API_URL, json=result_payload)
        return response.json()  # Return whatever the API responds with
    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": f"Failed to send result: {str(e)}"}