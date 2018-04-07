from urls import urls
import os.path
import re
import requests

SOURCE_RE = re.compile(r'source\.src = "(.*?)";')
BASE_URL = "https://www.destroyallsoftware.com/screencasts/catalog/"

for url in urls:
    # Go to the page with the video
    response = requests.get(url)
    doc = response.text

    # Grab the S3 video URL
    result = SOURCE_RE.search(doc, re.DOTALL)

    if not result:
        print("Could not get video for {} ".format(url))
        continue

    source = result.group(1)
    response = requests.get(source)

    # Download and save the video
    video_name = url.replace(BASE_URL, "")
    file_name = "videos/" + video_name + ".mp4"

    if os.path.isfile(file_name):
        print('{} already downloaded, skipping...'.format(video_name))
        continue

    print('Downloading {}...'.format(video_name))
    open(file_name, 'wb').write(response.content)
