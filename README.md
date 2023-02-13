# Content-Worker-API (Nightly Process)

This Python-based nightly worker API running on the cloud is designed to process, transcribe, and analyze content through a queue, while also checking for any infractions. The system is set up to run on a scheduled basis during the night to ensure that it can handle large volumes of content. The API uses speech-to-text technology to transcribe audio and video content, and then uses machine learning algorithms to analyze and identify any potential infractions. The API is designed to be scalable, allowing it to handle large volumes of content efficiently.

# Environment Setup 
Based on Fast API [Docs](https://fastapi.tiangolo.com/).

## Requirements
Python 3.7+ <br />
For Windows, use [Microsoft Store](https://www.microsoft.com/store/productId/9PJPW5LDXLZ5) to download the python release (Automatic Setup).

## Module Installations

FastAPI:
```
pip install fastapi
```

ASGI server - (Tested with [Uvicorn](https://www.uvicorn.org/)):
```
pip install "uvicorn[standard]"
```
Alternative ASGI server - ([Hypercorn](https://github.com/pgjones/hypercorn))

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

In your browser, once the server has started, open: <br/><br/>

Docs provided by [Swagger UI](https://github.com/swagger-api/swagger-ui):
```
http://127.0.0.1:8000/docs
```
Alternative Docs provided by [ReDoc](https://github.com/Redocly/redoc):
```
http://127.0.0.1:8000/redoc
```