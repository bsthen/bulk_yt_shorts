# from pytube import YouTube
# import ffmpeg

# ## download video from https://www.youtube.com/shorts/nlCZkdZl7C0
# ## separate audio and video to folder ./temp

# yt = YouTube("https://www.youtube.com/shorts/nlCZkdZl7C0")
# yt.streams.filter(file_extension='mp4').order_by('resolution').desc().first().download(filename="./temp/video.mp4")
# yt.streams.filter(only_audio=True).first().download(filename="./temp/audio.mp4")
# video = ffmpeg.input("./temp/video.mp4")
# audio = ffmpeg.input("./temp/audio.mp4")
# arguments = {
#     'c:v': 'copy',
#     'c:a': 'aac',
#     'b:a': '128k'
# }

# ffmpeg.run(ffmpeg.output(audio, video, "./temp/output.mp4", **arguments))