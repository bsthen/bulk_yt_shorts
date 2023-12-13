import yt_dlp
from pytube import YouTube
import ffmpeg
import shutil, os, platform

def is_windows():
    return platform.system() == "Windows"

def get_shorts(channel):
    
    if "youtube.com" not in channel:
        print("😢  Invalid youtube url. Exiting...\n")
        exit()
    elif channel == "":
        print("😢  No channel id given. Exiting...\n")
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
            print("😢  No shorts found\n")
            exit()
  
## download shorts high quality
def current_path():
    if is_windows():
        return os.getcwd().replace("\\", "/")
    else:
        return os.getcwd()

          
def download_shorts(short_links, save_path):
    save_path = save_path.replace('"', '')
    save_path = save_path.replace("'", "")
    if is_windows():
        save_path = save_path.replace("\\", "/")
    if not os.path.exists(save_path):
        print("😵  Error: Save path does not exist. Exiting...\n")
        exit()
    os.mkdir(save_path + "/temp")
    temp_dir = save_path + "/temp"
    ## found shorts
    print(f"🤩  Found {len(short_links)} video shorts\n")
        
    counter = 0  # Initialize a counter for numbering the files
    for short_link in short_links:
        ## check if video quality 1080p is available then download video and audio to temp and merge them by ffmpeg and delete temp files
        yt = YouTube(short_link)
        
        try:
            if yt.streams.filter(res="1080p").first() is not None:
                print(f"⬇️  Start Downloading {short_link} in 1080p\n")
                yt.streams.filter(file_extension='mp4').order_by('resolution').desc().first().download(filename=temp_dir + "/video.mp4")
                yt.streams.filter(only_audio=True).first().download(filename=temp_dir + "/audio.mp4")
                print("🔀  Merging video and audio...\n")
                video = ffmpeg.input(temp_dir + "/video.mp4")
                audio = ffmpeg.input(temp_dir + "/audio.mp4")
                arguments = {
                    'c:v': 'copy',
                    'c:a': 'aac',
                    'b:a': '128k',
                }
                ffmpeg.run(ffmpeg.output(audio, video, temp_dir + "/output.mp4", **arguments))
                os.remove(temp_dir + "/video.mp4")
                os.remove(temp_dir + "/audio.mp4")
                counter += 1  # Increment the counter
                shutil.move(temp_dir + "/output.mp4", f"{save_path}/{counter}.{yt.title}.mp4")
                os.remove(temp_dir + "/output.mp4")
                print("✅  Finish Downloaded: " + short_link + " in 1080p\n")
                
            elif yt.streams.filter(res="720p").first() is not None:
                yt.streams.filter(file_extension='mp4', res="720p").first().download(save_path, filename=temp_dir + "/output.mp4")
                video = ffmpeg.input(temp_dir + "/output.mp4")
                arguments = {
                    'c:v': 'copy',
                    'c:a': 'aac',
                    'b:a': '128k',
                }
                counter += 1  # Increment the counter
                ffmpeg.run(ffmpeg.output(video, f"{save_path}/{counter}.{yt.title}.mp4", **arguments))
                os.remove(temp_dir + "/output.mp4")
                print("✅  Finish Downloaded: " + short_link + " in 720p\n")
            else:
                print(f"🚫  Ohh! Video {short_link} is not available in 720p. Skipping...\n")
                continue
        except Exception as e:
            print(f"🚫  Ohh! error: {e}\n")
            continue
        
    shutil.rmtree(temp_dir)
    print(f"🥳  All shorts downloaded in {save_path}\n")
    print(f"🎉  Total shorts downloaded: {len(os.listdir(save_path))} | 💩 failed: {len(short_links) - len(os.listdir(save_path))}\n")


channel = input("📺  Enter Channel URL: ")
save_path = input("📂  Enter Location Directory: ")
shorts = get_shorts(channel)
download_shorts(shorts, save_path)