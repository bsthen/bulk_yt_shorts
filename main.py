import yt_dlp
from pytube import YouTube
import shutil, os, re
from moviepy.editor import VideoFileClip, AudioFileClip
from moviepy import config
import moviepy.video.fx.all as vfx
import platform
from multiprocessing import cpu_count
from  datetime import datetime

def set_ffmpeg_path():
    current_os = platform.system()
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ffmpeg_dir = os.path.join(script_dir, "ffmpeg")
    
    # if current_os == "Windows":
    #     ffmpeg_path = os.path.join(ffmpeg_dir, 'windows', 'ffmpeg.exe')
    # elif current_os == "Darwin":
    #     ffmpeg_path = os.path.join(ffmpeg_dir, 'macos', 'ffmpeg')
    # elif current_os == "Linux":
    #     ffmpeg_path = os.path.join(ffmpeg_dir, 'linux', 'ffmpeg')
    # else:
    #     raise Exception("Unsupported operating system")
    ffmpeg_path = os.path.join(ffmpeg_dir, 'ffmpeg.exe')
    
    config.change_settings({"FFMPEG_BINARY": ffmpeg_path})


def sanitize_filename(filename):
    unsupported_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']

    for char in unsupported_chars:
        filename = filename.replace(char, '_')
    
    filename = filename.strip()

    filename = re.sub('_+', '_', filename)

    return filename

def get_channel_id(channel):
    if "youtube.com" not in channel:
        print("😢  Invalid youtube url. Exiting...\n")
        input("Press any key to exit...")
        exit()
    elif channel == "":
        print("😢  No channel id given. Exiting...\n")
        input("Press any key to exit...")
        exit()
    elif "/@" in channel:
        channel = channel.split("/@")[1].split("/")[0]
        channel_url = f"https://www.youtube.com/@{channel}/shorts"
        return channel
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
    return channel

def get_shorts(channel):
    
    if "youtube.com" not in channel:
        print("😢  Invalid youtube url.\n")
        input("Press any key to exit...")
        exit()
    elif channel == "":
        print("😢  No channel id given.\n")
        input("Press any key to exit...")
        exit()
    elif "/@" in channel:
        channel = channel.split("/@")[1].split("/")[0]
        channel_url = f"https://www.youtube.com/@{channel}/shorts"
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
            input("Press any key to exit...")
            exit()
          
def download_shorts(short_links, save_path, videos_per_folder=20, speed=None, flip=False):
    set_ffmpeg_path()
    save_path = os.path.normpath(save_path)
    if not os.path.exists(save_path):
        print("😵  Error: Save path does not exist.\n")
        input("Press any key to exit...")
        exit()
    temp_dir = os.path.join(save_path, "temp")
    if not os.path.exists(temp_dir):
        os.mkdir(temp_dir)
        
    if not temp_dir.endswith(os.sep):
        temp_dir += os.sep
        
    print(f"🤩  Found {len(short_links)} video shorts\n")

    folder_counter = 0
    folder_path = os.path.join(save_path, str(folder_counter + 1))
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
        
    folder_video_counter = 1

    for short_link in short_links:
        yt = YouTube(short_link)
        try:
            if yt.streams.filter(res="1080p").first() is not None:
                files = os.listdir(temp_dir)
                for file in files:
                    os.remove(os.path.join(temp_dir, file))
                print(f"⬇️  Start Downloading {short_link} in 1080p at ⌚️{datetime.now().strftime('%d-%m-%Y %I:%M:%S %p')}\n")
                yt.streams.filter(file_extension='mp4').order_by('resolution').desc().first().download(filename=temp_dir + "video.mp4")
                yt.streams.filter(only_audio=True).first().download(filename=temp_dir + "audio.mp3")
                print(f"✅  Finish Downloaded: {short_link} in 1080p at ⌚️{datetime.now().strftime('%d-%m-%Y %I:%M:%S %p')}\n")
                print(f"✂️ Editing Video {short_link} in 1080p at ⌚️{datetime.now().strftime('%d-%m-%Y %I:%M:%S %p')}\n")
                video = VideoFileClip(temp_dir + "video.mp4")
                audio = AudioFileClip(temp_dir + "audio.mp3")
                video = video.set_audio(audio)
                if speed is not None:
                    video = video.fx(vfx.speedx, float(speed))
                if flip is True:
                    video = video.fx(vfx.mirror_x)
                files_in_folder = len([f for f in os.listdir(folder_path) if f.endswith('.mp4')])
                if files_in_folder >= int(videos_per_folder):
                    folder_counter += 1
                    folder_path = os.path.join(save_path, str(folder_counter + 1))
                    if not os.path.exists(folder_path):
                        os.mkdir(folder_path)
                    folder_video_counter = 1
                video.write_videofile(os.path.join(folder_path, f"{sanitize_filename(yt.title)}_{folder_video_counter}.mp4"), verbose= False, codec="libx264", audio_codec="aac", logger= None, threads=cpu_count())
                folder_video_counter += 1
                print(f"✅  Finish Video: {short_link} in 1080p at ⌚️{datetime.now().strftime('%d-%m-%Y %I:%M:%S %p')}\n")
                
            elif yt.streams.filter(res="720p").first() is not None:
                print(f"⬇️  Start Downloading {short_link} in 720p at ⌚️{datetime.now().strftime('%d-%m-%Y %I:%M:%S %p')}\n")
                yt.streams.filter(file_extension='mp4', res="720p").first().download(filename=temp_dir + "output.mp4")
                print(f"✅  Finish Downloaded: {short_link} in 720p at ⌚️{datetime.now().strftime('%d-%m-%Y %I:%M:%S %p')}\n")
                print(f"✂️ Editing Video {short_link} in 720p at ⌚️{datetime.now().strftime('%d-%m-%Y %I:%M:%S %p')}\n")
                video = VideoFileClip(temp_dir + "output.mp4")
                if speed is not None:
                    video = video.fx(vfx.speedx, float(speed))
                if flip is True:
                    video = video.fx(vfx.mirror_x)
                files_in_folder = len([f for f in os.listdir(folder_path) if f.endswith('.mp4')])
                if files_in_folder >= int(videos_per_folder):
                    folder_counter += 1
                    folder_path = os.path.join(save_path, str(folder_counter + 1))
                    if not os.path.exists(folder_path):
                        os.mkdir(folder_path)
                    folder_video_counter = 1
                video.write_videofile(os.path.join(folder_path, f"{sanitize_filename(yt.title)}_{folder_video_counter}.mp4"),verbose= False, codec="libx264", audio_codec="aac", logger= None, threads=cpu_count())
                folder_video_counter += 1
                print(f"✅  Finish Video: {short_link} in 720p at ⌚️{datetime.now().strftime('%d-%m-%Y %I:%M:%S %p')}\n")
            else:
                print(f"🚫  Ohh! Video {short_link} is not available in 720p. Skipping...\n")
                continue
        except Exception as e:
            print(f"🚫  Ohh! error: {e}\n")
            continue
        
    shutil.rmtree(temp_dir)
    
    print(f"🥳  All shorts downloaded in {save_path}\n")

def welcome_message():
    large_text = """
     ____        _ _       _____ _                _         _____                      _                 _           
    |  _ \      | | |     / ____| |              | |       |  __ \                    | |               | |          
    | |_) |_   _| | | __ | (___ | |__   ___  _ __| |_ ___  | |  | | _____      ___ __ | | ___   __ _  __| | ___ _ __ 
    |  _ <| | | | | |/ /  \___ \| '_ \ / _ \| '__| __/ __| | |  | |/ _ \ \ /\ / / '_ \| |/ _ \ / _` |/ _` |/ _ \ '__|
    | |_) | |_| | |   <   ____) | | | | (_) | |  | |_\__ \ | |__| | (_) \ V  V /| | | | | (_) | (_| | (_| |  __/ |   
    |____/ \__,_|_|_|\_\ |_____/|_| |_|\___/|_|   \__|___/ |_____/ \___/ \_/\_/ |_| |_|_|\___/ \__,_|\__,_|\___|_|   
    
                                                                                                     v1.0.12 | @bsthen                                                                                                              
                                                                                                                  
    """
    print(large_text)

def main():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        welcome_message()
        
        print("Choose an option:\n")
        print("☝️ 1. Download shorts from a Channel URL")
        print("✌️ 2. Download shorts from a batch file.txt\n")
        print("🚪 Press any other key to exit\n")
        
        choice = input("👉  Enter your choice: ").strip().lower()
        
        if choice == "1":
            channel = input("\n📺  Enter Channel URL: Ex. https://www.youtube.com/@123/shorts\n --> ")
            if "youtube.com" not in channel:
                print("😢  Invalid youtube url.\n")
                input("Press any key to exit...")
                exit()
            save_path = input("\n📂  Enter Download Directory: Ex. D:\\Download\\Short\\\n --> ")
            if not os.path.exists(save_path):
                print("😵  Error: Save path does not exist.\n")
                input("Press any key to exit...")
                exit()
            videos_per_folder = input("\n📁  Enter Number #Videos Per Folder: Ex. 20\n --> ")
            if not videos_per_folder.isdigit():
                print("😢  Invalid Number.\n")
                input("Press any key to exit...")
                exit()
            add_speed = input("\n🏃  Do you want to add speed? (y/n): ").strip().lower()
            if add_speed == "y":
                speed = input("\n🏃  Enter Speed: Ex. 1.2\n --> ")
                speed = float(speed)
                if not isinstance(speed, float or int):
                    print("😢  Invalid Speed.\n")
                    input("Press any key to exit...")
                    exit()
            else:
                speed = None
            add_flip = input("\n🔄  Do you want to add flip? (y/n): ").strip().lower()
            if add_flip == "y":
                flip = True
            else:
                flip = False
            shorts = get_shorts(channel)
            download_shorts(shorts, save_path, videos_per_folder, speed, flip)
            break
        elif choice == "2":
            channel_list = input("\n📺  Enter A Batch File.txt: Ex. D:\\Download\\Short\\AnyName.txt\n --> ")
            if not os.path.exists(channel_list):
                print("😢  Invalid batch file.\n")
                input("Press any key to exit...")
                exit()
            save_path = input("\n📂  Enter Download Directory: Ex. D:\\Download\\Short\\\n --> ")
            if not os.path.exists(save_path):
                print("😵  Error: Save path does not exist.\n")
                input("Press any key to exit...")
                exit()
            videos_per_folder = input("\n📁  Enter Number #Videos Per Folder: Ex. 20\n --> ")
            if not videos_per_folder.isdigit():
                print("😢  Invalid number.\n")
                input("Press any key to exit...")
                exit()
            add_speed = input("\n🏃  Do you want to add speed? (y/n): ").strip().lower()
            if add_speed == "y":
                speed = input("\n🏃  Enter Speed: Ex. 1.2\n --> ")
                if not speed.isdigit():
                    print("😢  Invalid Speed.\n")
                    input("Press any key to exit...")
                    exit()
            else:
                speed = None
            add_flip = input("\n🔄  Do you want to add flip? (y/n): ").strip().lower()
            if add_flip == "y":
                flip = True
            else:
                flip = False
            with open(channel_list, "r") as f:
                for channel in f:
                    if "youtube.com" not in channel:
                        print("😢  Invalid YouTube Channel! Make Sure All URL Are Correct And 1 Channel URL Per Line.\n")
                        input("Press any key to exit...")
                        exit()
                    ## get channel id and create folder
                    channel_id = get_channel_id(channel)
                    ## create folder
                    path_channel = os.path.join(save_path, channel_id)
                    if not os.path.exists(path_channel):
                        os.mkdir(path_channel)
                    shorts = get_shorts(channel)
                    download_shorts(shorts, path_channel, videos_per_folder, speed, flip)
            break
        else:
            print("😢  Invalid choice. Exiting...\n")
            input("Press any key to exit...")
            exit()

if __name__ == "__main__":
    main()
    input("Press any key to exit...")
    exit()