import ffmpeg
import os
import shutil
import tkinter as tk
from tkinter import filedialog

def get_video_duration(video_path):
    """Get the duration of a video in seconds."""
    probe = ffmpeg.probe(video_path)
    duration = float(probe['streams'][0]['duration'])
    return duration

def compress_videos(folder_location, convert_in_place):
    """Compresses all the videos in a folder and its subfolders."""
    if not convert_in_place:
        converted_folder_location = os.path.join(folder_location, "converted")
        if not os.path.exists(converted_folder_location):
            os.mkdir(converted_folder_location)

    for root, dirs, files in os.walk(folder_location):
        for file in files:
            if file.endswith(".mp4"):
                video_file = os.path.join(root, file)

                if convert_in_place:
                    output_path = video_file.replace('.mp4', '_temp.mp4')
                else:
                    output_path = os.path.join(folder_location, "converted", os.path.relpath(video_file, folder_location))
                    output_directory = os.path.dirname(output_path)
                    if not os.path.exists(output_directory):
                        os.makedirs(output_directory)

                ffmpeg.input(video_file).output(
                    output_path, 
                    **{
                        'c:v': "libx264", 
                        'preset': "veryfast", 
                        'crf': "28", 
                        'b:a': "64k", 
                        'c:a': "aac", 
                        'strict': "experimental"
                    }
                ).overwrite_output().run()

                if convert_in_place:
                    os.remove(video_file)
                    shutil.move(output_path, video_file)

# Create a basic tkinter window
root = tk.Tk()
root.withdraw()  # Hide the main window

# Use tkinter's filedialog to ask for folder location
folder_location = filedialog.askdirectory(title="Select a folder containing the video files to be converted")

if not folder_location:
    print("No folder selected. Exiting...")
    exit()

convert_in_place = input("Do you want to convert the videos in place (y) or save them to a converted folder (n)? ") == "y"
compress_videos(folder_location, convert_in_place)
