from moviepy.editor import VideoFileClip
# from moviepy.video.io.ffmpeg_tools import VideoFileClip
# ^^ cut these down
import websockets
from datetime import datetime
import asyncio
import json
import platform
# import AS3_uploader
import os
import urllib.request
print("initialized")

VIDEO_PATH = os.getcwd() + "/" + "test files/video1.mp4"
CLIP_PATH = os.getcwd() + "/" + "output files/video_segment.mp4"
AUDIO_PATH = os.getcwd() + "/" + "output files/audio_segment.mp4"
OUTPUT_PATH = os.getcwd() + "/" + "output files/full_video.mp4"

if platform.system() == "Windows":
  # Windows uses a backslash, mac and unix based uses a forward slash
  VIDEO_PATH = VIDEO_PATH.replace("/", "\\")
  CLIP_PATH = CLIP_PATH.replace("/", "\\")
  AUDIO_PATH = AUDIO_PATH.replace("/", "\\")
  OUTPUT_PATH = OUTPUT_PATH.replace("/", "\\")


def get_clip(host_url, start, end, url=""):
  try:
    urllib.request.urlretrieve(host_url, VIDEO_PATH) 
  except:
    pass
  initialtime = datetime.now()
  video = VideoFileClip(VIDEO_PATH, verbose=False)

  # Create a subclip from the video
  subclip = video.subclip(start, end)

  # Write the subclip to a new video file
  subclip.write_videofile(OUTPUT_PATH, fps=24, verbose=False, logger=None)


  print("\n[Video Cutter] Cutting clip from time " + str(start) + " to " + str(end))
  print("[Video Cutter] Took " + str(datetime.now() - initialtime) + " seconds")

  config = json.loads(os.read("config.json", "r"))

  # AS3_uploader.upload_file(config["bucket-name"], config["folder-name"], "Back\\output files\\full_video.mp4", "video.mp4")

async def get_clip_bytes(websocket):

    host_url = "" # change this to the url from which to get the video, feel free to modify getting it in some way



    # get variables, websocket is a websocketserverprotocol object, not the in data
    input_data = await websocket.recv()
    # Preventing JSON bombs
    if len(input_data) < 200:
      # ignore empty or invalid data
      try:
        input_data_dict = json.loads(input_data)
        get_clip(host_url, input_data_dict["start_timestamp"], input_data_dict["end_timestamp"])
        # await websocket.send(bytes(open(OUTPUT_PATH, "r").read()))
      except Exception as e:
        # prints error in case it is not empty or invalid data related
        if "'utf-8'" not in str(e) and "bounds" not in str(e):
          print(e)

# todo - run get_clip 

async def main(): 
  async with websockets.serve(get_clip_bytes, "", 8765):
    await asyncio.Future()

if __name__ == "__main__":
  asyncio.run(main())
