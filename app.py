from fastapi import FastAPI, File, UploadFile
import os
import logging
from predict import predict
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

@app.get("/")
async def root():
    return { "message" : "Pakinson's" }

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    # logging.info("Received request to create_upload_file")
    uploads_dir = "uploads"
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir)
    file_location = f"{uploads_dir}/{file.filename}"
    with open(file_location, "wb") as file_object:
        file_object.write(file.file.read())
    result=predict(file_location)
    # print("Received request to create_upload_file")
    # print(f"File name: {file.filename}")
    return {"filename": file.filename, "result":result}


# Allow all domains to make requests to the API
origins = ["*"]

# Configure the CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)