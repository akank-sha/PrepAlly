from fastapi import FastAPI, status, UploadFile, HTTPException
from uuid import uuid4
import os
import json
from summarizer_model_abstraction import generateQuestionsFromCorpus
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# AWS_BUCKET = "prepally"
# s3 = boto3.resource("s3")
# bucket = s3.Bucket(AWS_BUCKET)


# async def upload_to_s3(contents: bytes, name: str):
#     return await bucket.put_object(Body=contents, Key=name)

print("done")
KB = 1024
MB = 1024 * KB

cache = {}
with open("cache.json", "r") as f:
    cache = json.load(f)


@app.get("/")
async def root():
    global cache
    with open("cache.json", "r") as f:
        cache = json.load(f)
    return {"healthCheck": "ok"}


@app.post("/uploadFile")
async def upload(file: UploadFile | None = None):
    global cache
    if file is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No file provided"
        )
    contents = await file.read()
    file_size = len(contents)

    if not 0 < file_size <= 50*MB:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Supported file size is 0 - 50MB'
        )
    fileName = f"{uuid4()}.txt"
    try:

        with open(f"./data/{fileName}", "wb") as f:
            f.write(contents)
    except Exception as e:
        print(e)
        os.mkdir("./data")
        with open(f"./data/{fileName}", "wb") as f:
            f.write(contents)
    f = open(f"./data/{fileName}", "r", encoding="utf-8")
    fileContents = f.read()
    if (fileContents[:50] in cache):
        return cache[fileContents[:50]]
    result = generateQuestionsFromCorpus(fileContents)
    cache[fileContents[:50]] = result
    with open("cache.json", "w") as f:
        json.dump(cache, f)
    return result
