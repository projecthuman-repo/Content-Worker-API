# Content-Worker-API (Nightly Process)

This Python-based nightly worker API running on the cloud is designed to process, transcribe, and analyze content through a queue, while also checking for any infractions. The system is set up to run on a scheduled basis during the night to ensure that it can handle large volumes of content. The API uses speech-to-text technology to transcribe audio and video content, and then uses machine learning algorithms to analyze and identify any potential infractions. The API is designed to be scalable, allowing it to handle large volumes of content efficiently.

# Environment Setup

Based on Fast API [Docs](https://fastapi.tiangolo.com/).

## Requirements

Python 3.7+ `<br />`
For Windows, use [Microsoft Store](https://www.microsoft.com/store/productId/9PJPW5LDXLZ5) to download the python release (Automatic Setup).

## Module Installations

Use this command to install all the modules automatically (Like npm install):

```
pip install -r .\packages.txt
```

## Running The Server (For Development)

Main Command:

```
uvicorn main:app --reload
```

Alternative Command - If above returns an error of uvicorn not detected

```
python -m uvicorn main:app --reload
```

## Accessing the Server

In your browser, open:

```
http://127.0.0.1:8000
```

## Interactive Docs

The docs are generated dynamically based on the code in the server files.

In your browser, once the server has started, open: `<br/><br/>`

Docs provided by [Swagger UI](https://github.com/swagger-api/swagger-ui):

```
http://127.0.0.1:8000/docs
```

Alternative Docs provided by [ReDoc](https://github.com/Redocly/redoc):

```
http://127.0.0.1:8000/redoc
```

## **Image and Video Moderation usage Docs:**

**Step 1:**

Create .env file 

```
RESULT_API_URL= http://localhost:8080/result
```

```
IMAGE_MODEL_PATH = 'Content-Worker-API/image_model/nsfw_model/merged_trained_nsfw_mobilenet_224x244_30.h5'
```

```
VIDEO_MODEL_PATH = "VideoMAE/videomae-small-finetuned-kinetics-finetuned-ucf101-subset" # other are base, large
```

Update the image model path in `Content-Worker-API/modules/image_moderation.py `

Update the Video model path in `Content-Worker-API/modules/video_moderation.py`

**Step 2:**

```
http://127.0.0.1:8000/moderate/file
```

POST methods should contain the following parameters

```
payload = {
        documentID: documentID,
        data : contentURL, #"link to download text or text itself"
        contentDetails: {
          contentType: "text", #"placeholder"
          contentLength:1024, # number of words
          timestamp: 31/12/1025 #(or something like that) from Date().toISOString()
        }
      }
```

FileType is optional and can be `image` , `video` or `unknown`
