#!/usr/bin/env python
from pymongo import MongoClient
from bson.objectid import ObjectId
import os, sys, pika, gridfs
from moviepy import *

# MongoDB credentials
username = "admin"
password = "password"

# MongoDB connection string with credentials
connection_string = f"mongodb://{username}:{password}@mongodb:27017/"

# Connect to MongoDB (Docker local)
client = MongoClient(connection_string)
db = client["media_database"]  # Use or create a database
fs = gridfs.GridFS(db)


def convert_video_to_audio(file_id):
    file_id = ObjectId(file_id)
    file_data = fs.get(file_id)
    output_path = "temp.mp4"
    
    with open(output_path, "wb") as output_file:
        output_file.write(file_data.read())

        print(f"Retrieved file saved to {output_path}")

    audio_filename = "temp.mp3"
    video_clip = VideoFileClip(output_path)
    video_audio = video_clip.audio
    video_audio.write_audiofile(audio_filename)

    with open("temp.mp3", "rb") as file_data:
        file_id = fs.put(file_data, filename=audio_filename, content_type="audio/mpeg")
        print(f"Stored {audio_filename} with ID: {file_id}")

    return file_id


def main():
    connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    channel.queue_declare(queue='task_queue', durable=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')


    def callback(ch, method, properties, body):
        print(f" [x] Received {body.decode()}")
        try:
            convert_video_to_audio(body.decode())
            ch.basic_ack(delivery_tag=method.delivery_tag)
            print("Completed conversion")
        except Exception as e:
            print(e)
            ch.basic_ack(delivery_tag=method.delivery_tag)


    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='task_queue', on_message_callback=callback)

    channel.start_consuming()


if __name__ == '__main__':
    print("Bruh")
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)