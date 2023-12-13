import yt_dlp
from pytube import YouTube
import os

def get_shorts(channel):
    
    if "youtube.com" not in channel:
        print("Invalid youtube url. Exiting...")
        exit()
    elif channel == "":
        print("No channel id given. Exiting...")
        exit()
    elif "/@" in channel:
        channel = channel.split("/@")[1].split("/")[0]
        channel_url = f"https://www.youtube.com/@{channel}/shorts"
        # print("Channel url: " + channel_url)
    else:
        channel = channel.split("/about")[0]
        channel = channel.split("/channel/")[1]
        channel = channel.split("/c/")[1]
        channel = channel.split("/user/")[1]
        channel = channel.split("/community")[0]
        channel = channel.split("/featured")[0]
        channel = channel.split("/videos")[0]
        channel = channel.split("/discussion")[0]
        channel = channel.split("/playlists")[0]
        channel = channel.split("/channels")[0]
        channel = channel.split("/feed")[0]
        channel = channel.split("/live")[0]
        channel = channel.split("/about")[0]
        channel = channel.split("/stream")[0]
        channel = channel.split("/playlists")[0]
        
        channel += "/shorts"
        # print("Channel id: " + channel)
        
    with yt_dlp.YoutubeDL() as ydl:
        result = ydl.extract_info(channel_url, download=False, process=False)
        if 'entries' in result:
            video_ids = [entry['id'] for entry in result['entries']]
            short_links = [f"https://www.youtube.com/shorts/{video_id}" for video_id in video_ids]
            return short_links
        else:
            print("No shorts found")
            exit()
  
## download shorts high quality
          
def download_shorts(short_links, save_path):
    save_path = save_path.replace('"', '')
    save_path = save_path.replace("'", "")
    print(save_path)
    if not os.path.exists(save_path):
        print("Error: Save path does not exist. Exiting...")
        exit()
    print(f"Downloading shorts in {os.getcwd()}/shorts")
        
    for short_link in short_links:
        yt = YouTube(short_link)
        try:
            print("Start Downloading: " + short_link)
            yt.streams.filter(file_extension='mp4', res="720p").first().download(save_path)
            print("Finish Downloaded: " + short_link)
        except:
            print("Video {short_link} is not available in 720p. Skipping...")
            continue
    print(f"All shorts downloaded in {os.getcwd()}/shorts")


channel = input("Enter Channel URL: ")
save_path = input("Enter save path: ")
shorts = get_shorts(channel)
download_shorts(shorts, save_path)