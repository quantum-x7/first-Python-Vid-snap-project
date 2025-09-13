#This Files look for new folder inside the user-uploads then proceess them to reel if they are not already converted
import os,time,subprocess
from text_to_audio import text_to_speech_file
# TTA
def text_to_audio(folder):
    print("TTA - ",folder)
    with open(f"user_uploads/{folder}/desc.txt", encoding="utf-8") as f:
        text = f.read()

    print(text,folder)
    text_to_speech_file(text,folder)
    
def create_reel(folder):
    command = f'''ffmpeg -f concat -safe 0 -i user_uploads/{folder}/input.txt -i user_uploads/{folder}/audio.mp3 -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" -c:v libx264 -c:a aac -shortest -r 30 -pix_fmt yuv420p static/reels/{folder}.mp4'''
    
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.returncode != 0:
        print("FFmpeg failed!")
        print("STDERR:", result.stderr)
    else:
        print("CR - ", folder)


if __name__ == '__main__':
    while True:
        print("Processing Qeue.....")
        with open('done.txt','r') as f:
            done_folders = f.readlines()
            done_folders = [f.strip() for f in done_folders]
        folders = os.listdir("user_uploads")
        for folder in folders:
            if folder not in done_folders:
                text_to_audio(folder) # genrate audio.mp3 from the desc.txt
                create_reel(folder) # converte images and audio.mp3 to REEL
                with open('done.txt' , 'a') as f:
                    f.write(folder + '\n')
        time.sleep(4)