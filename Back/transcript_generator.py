from stable_whisper import load_model
import ffmpeg
import os
import platform
print(ffmpeg.__file__)
# model = whisper.load_model('base')

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

# static variables copy pasted from websocket clipper instead of imported. This is so it can run in a separate VM due to different python versions without having to import all the packages separately



# assert model.transcribe(PATH_TO_FILE).get('segments')


model = load_model('base')
# modified model should run just like the regular model but with additional hyperparameters and extra data in results
print(VIDEO_PATH)
results = model.transcribe(VIDEO_PATH)
stab_segments = results['segments']
first_segment_word_timestamps = stab_segments[0]['whole_word_timestamps']

# or to get token timestamps that adhere more to the top prediction
from stable_whisper import stabilize_timestamps
stab_segments = stabilize_timestamps(results, top_focus=True)

word_timestamp_dict = {}
# unstable_word_timestamps

fd = open("transcript.txt", "w")
# fd.write(str(stab_segments))
for i in stab_segments:
    for j in i["unstable_word_timestamps"]:
        # iterate over a list of dicts, each dict having data on one word
        if (j["word"]) in word_timestamp_dict:
            # check if word has been seen before, if so add to the prior key value pair
            # valuelist = [(list(set(round(num, 1)))).sort() for num in j["timestamps"]]
            # word_timestamp_dict[j["word"]].extend(valuelist)
            pass
        else:
            # if word has not been seen before, add key value pair to word_timestamp_dict

            # round timestamp values to the closest tenth of a second, remove duplicate values, sort in ascending order.
            # it uses a list comprehension, to round the values, then uses the builtin methods set, list, and sort in that order.
            valuelist = [(round(num, 1)) for num in j["timestamps"]]
            valuelist = list(set(valuelist))
            valuelist.sort()
            word_timestamp_dict[j["word"]] = valuelist

fd.write(str(word_timestamp_dict))