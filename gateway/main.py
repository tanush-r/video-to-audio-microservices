import os, pika, sys
import gridfs
from pymongo import MongoClient
from bson.objectid import ObjectId
import logging
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse


# Initialize FastAPI app
app = FastAPI()


# Connect to MongoDB (Docker local)
client = MongoClient("mongodb://localhost:27017/")
db = client["media_database"]  # Use or create a database
fs = gridfs.GridFS(db)

# RabiitMQ sender using Pika(One piece reference?)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    file_content = await file.read()
    file_id = fs.put(file_content, filename=file.filename, content_type="video/mp4")
    file_id = str(file_id)
    channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        body=file_id,
        properties=pika.BasicProperties(
            delivery_mode=pika.DeliveryMode.Persistent
        ))

    return {"message": f"{file.filename} pushed to queue, Await email", "file_id": file_id}


@app.get("/download_audio")
async def download_audio(file_id: str):

    file_id = ObjectId(file_id)
    output_path = "temp.mp3"
    file_data = fs.get(file_id)
    with open(output_path, "wb") as output_file:
        output_file.write(file_data.read())
        print(f"Retrieved file saved to {output_path}")

    # Serve the file for download
    headers = {
        "Content-Disposition": f"attachment; filename={os.path.basename(output_path)}"
    }
    return FileResponse(path=output_path, media_type="audio/mpeg", headers=headers)
