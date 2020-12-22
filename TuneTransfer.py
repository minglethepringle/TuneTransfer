import os
import shutil
import subprocess
import webbrowser
from itertools import islice
from pyyoutube import Api
import youtube_dl

API_KEY = [APIKEY]
PLAYLIST_ID = "PL5Y2tGfke7b64Qa1OR5l26a8dgXx4tWUg"
DOWNLOAD_DIR_NAME = "downloaded"
SEARCH_COUNT = 5

api = Api(api_key=API_KEY)

def already_downloaded(video_id):
    with open("already_downloaded.txt") as myfile:
        # Read SEARCH_COUNT lines of file and strip \n
        downloaded_list = [x.rstrip("\n") for x in islice(myfile, SEARCH_COUNT)] 
    return video_id in downloaded_list
    
def download_videos_mp3(video_name_list, video_id_list):
    print("Downloading MP3s!")

    for i in range(0, len(video_id_list)):
        # Save mp3 to downloaded directory
        SAVE_PATH = os.path.join(os.getcwd(), DOWNLOAD_DIR_NAME, video_name_list[i])

        ydl_opts = {
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
            "outtmpl": SAVE_PATH + ".", # added . to fix ydl bug of expecting extension to replace
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_id_list[i]])

def zip_music():
    shutil.make_archive("music", "zip", DOWNLOAD_DIR_NAME)

def save_video_ids(video_id_list):
    id_string = "\n".join(video_id_list) + "\n"
    # Prepending is inefficient for memory. Write id_string to new file and append old file contents
    with open("already_downloaded.txt", "r") as f:
        with open("temp.txt", "w") as f2: 
            f2.write(id_string)
            f2.write(f.read())
    os.rename("temp.txt", "already_downloaded.txt")

def main():
    music_playlist = api.get_playlist_items(playlist_id=PLAYLIST_ID, count=SEARCH_COUNT)

    download_names = []
    download_ids = []
    for video in music_playlist.items:
        video_id = video.snippet.resourceId.videoId
        print("Got video ID:", video_id)
        # If the video ID is not already downloaded,
        if not already_downloaded(video_id):
            video_name = video.snippet.title
            download_names.append(video_name)
            download_ids.append(video_id)
    
    if len(download_ids) > 0:
        print("Need to download list: " + str(download_ids))
        # Create downloaded folder if it doesn't exist
        if not os.path.exists(DOWNLOAD_DIR_NAME):
            print("Dir does not exist, creating...")
            os.makedirs(DOWNLOAD_DIR_NAME)

        # Create formatted video ID list for ydl
        video_links_list = ["http://www.youtube.com/watch?v={0}".format(x) for x in download_ids]
        download_videos_mp3(download_names, video_links_list)

        # Compress music directory to ZIP
        zip_music()

        # Save video IDs into already_downloaded.txt
        save_video_ids(download_ids)

        # Delete downloaded mp3s folder
        shutil.rmtree(DOWNLOAD_DIR_NAME)

        # Open up Finder and Sharedrop.io
        webbrowser.get(using='open -a /Applications/Google\ Chrome.app %s').open("https://sharedrop.io")
        subprocess.call(["open", "-R", "/Users/mingle_li/Dropbox/PythonWorkspace/TuneTransfer/music.zip"])

if __name__ == "__main__":
    main()