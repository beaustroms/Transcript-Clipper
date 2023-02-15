-- Backend Instructions:


To generate transcripts: run transcript generator (must have stable whisper installed, use 

pip install git+https://github.com/jianfch/stable-ts.git 

to install it), you also must have ffmpeg-python installed (use pip) and must be on python 3.8. This is due to whisper not supporting futher versions. Whisper might support 3.9, but I have encountered a segfault issue running on 3.9. To run a separate python version, I recommend using a venv. Anaconda can do this easily. 

Transcript generator will check for a file in Back/test files/video1.mp4, you can change this to whatever you prefer.

It will write a file to output files/transcript.json, which has a set of key value pairs in the format "word":[seconds], seconds being a list of the timestamp of each occurance of the word in order.


Running the websocket backend server:

Run websocket_clipper.py, not too much else is needed. It will open up a websocket server which will be contacted by the JS script. This websocket server will recieve the starting time and ending time in JSON format from the javascript server, and will then generate a clip of the file at the url specified at the beginning of the get_clip_bytes function (that url is for wherever the video to be clipped is hosted). It then saves it to Back/output files/full_video.mp4, which is uploaded to S3 via a call to AS3_uploader.py

You need an AS3 environment variable set under "AS3_Secret" or AS3_uploader will not work



-- Frontend Instructions:

Add < script src="get_selection.js" > without the spaces to your html file. Connect this to the python websocket server (default connected to ws://localhost:8765). The script will look for elements which have the id of transcript, they must have data-JSONtimestamps as a JSON of words paired with their timestamps in seconds. onmouseup=getText() also must be included, as it gets the highlighted text.


