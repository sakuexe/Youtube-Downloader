# Downloader for Youtube videos in python
# Written in Python 3.10.7 - 12/1/2023

import yt_dlp as youtube_dl
import os
from Terminal_Effects import tcolors, clear_terminal

# The text that is shown at the start to the user
start_info = [
	f"{tcolors.cyan}Youtube Downloader{tcolors.clear}", 
	f"{tcolors.gray}Written in Python 3.10.7 - 12/1/2023",
	"By SakuK" + tcolors.clear,
]

# options for the user to choose from
options = [
	"Choose what format do you want to download",
	"---",
	f"{tcolors.yellow}1){tcolors.clear} Audio only in mp3",
	f"{tcolors.yellow}2){tcolors.clear} Audio only in webm",
	f"{tcolors.yellow}3){tcolors.clear} Video & Audio in mp4",
	f"{tcolors.yellow}4){tcolors.clear} Video & Audio in webm",
]

playlist_options = [
	"do you want to download a playlist?",
	"y/n"
]

# This function is called when the download is finished
def my_hook(d):
    if d['status'] == 'finished':
        print('\nDone downloading, now converting ...')

# Fetch the location of the user's desktop, this is where the file is downloaded to
desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

# The options for youtube-dl
ydl_opts = {
	'format': 'bestaudio/best',
	'outtmpl': desktop + '/%(title)s.%(ext)s',
	'noplaylist' : True,
	'progress_hooks': [my_hook],
}

# This function is called when the user inputs their choice
def process_choice(choice):
	# pseudo switch case for different choices
	if choice == "1":
		ydl_opts["format"] = "bestaudio/best"
		ydl_opts["postprocessors"] = [{
			'key': 'FFmpegExtractAudio',
			'preferredcodec': 'mp3',
			'preferredquality': '192',
		}]
		return
	if choice == "2":
		ydl_opts["format"] = "bestaudio/best"
		return
	if choice == "3":
		ydl_opts["format"] = "bestvideo+bestaudio/best"
		ydl_opts["postprocessors"] = [{
			'key': 'FFmpegVideoConvertor',
			'preferedformat': 'mp4',
		}]
		return
	if choice == "4":
		ydl_opts["format"] = "bestvideo+bestaudio/bestvideo/best"
		return
	else:
		# if the user doesn't type a valid choice, raise an exception
		Exception("Invalid choice")

def main():
	print(clear_terminal.clear())
	print("\n".join(start_info))
	print("---")
	print("\n".join(options))
	print()
	user_choice = input("Input your choice (numerically): ")

	try:
		# Process the choice that the user input and change the ydl_opts accordingly
		process_choice(user_choice)
	except Exception as e:
		print(e)
		input("press enter to quit")
		return

	# Ask the user if they want to download a playlist
	print("\n".join(playlist_options))
	playlist_choice = input()

	# process the choice of the user
	if playlist_choice == "y":
		ydl_opts["noplaylist"] = False
	elif playlist_choice == "n":
		ydl_opts["noplaylist"] = True
	else:
		# if the user doesn't type a valid choice, return and reset
		input("press enter to try again")
		main()
		return

	# Next ask the user for a link to the video
	link = input("Input the link to the video: ")
	print(clear_terminal.clear())
	if ydl_opts["noplaylist"] == True:
		print(f"{tcolors.gray}downloading video info...{tcolors.clear}")
		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			info = ydl.extract_info(link, download=False)
		print(clear_terminal.clear())
		print(f"upload date: %s" % tcolors.yellow, info["title"], tcolors.clear)
		print(f"upload date: %s" % tcolors.yellow, info["upload_date"], tcolors.clear)
		print("uploader: %s" % tcolors.yellow, info["uploader"], tcolors.clear)
		print("view count: %s" % tcolors.yellow, info["view_count"], tcolors.clear)
		print("format: %s" % tcolors.yellow, info["format"], tcolors.clear)
		print("duration: %s" % tcolors.yellow, info["duration"], tcolors.clear)

		print("is this the correct video? (y/n)" + tcolors.cyan)
		correct_video = input()
	else:
		print(f"{tcolors.gray}downloading playlist info...{tcolors.clear}")
		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			info = ydl.extract_info(link, download=False)
			print(clear_terminal.clear())
			print(f"title: %s" % tcolors.yellow, info["title"], tcolors.clear)
			print(f"description: %s" % tcolors.yellow, info["description"], tcolors.clear)
			print("uploader: %s" % tcolors.yellow, info["uploader"], tcolors.clear)
			print("amount of videos: %s" % tcolors.yellow, info["playlist_count"], tcolors.clear)

		print("is this the correct playlist? (y/n)" + tcolors.cyan)
		correct_video = input()
	tcolors.clear

	try:
		# Check if the link is of the correct video
		if correct_video == "y" and ydl_opts["noplaylist"] == True:
			print("downloading video to desktop...")
			download_video(ydl_opts, link)
			end_info(info["title"])
			# end_info(info["title"] + "." + info["ext"])
		if correct_video == "y" and ydl_opts["noplaylist"] == False:
			print("downloading playlist to desktop...")
			download_video(ydl_opts, link)
			end_info(info["title"])
		else:
			# if not, ask the user if they want to try again
			print("press enter to try again")
			input()
			# rerun the main function
			main()
			return
	except Exception as e:
		print("Error occured: " + f"{tcolors.red}" + str(e) + f"{tcolors.clear}")

def download_video(ydl_opts, link):
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		ydl.download([link])

def end_info(filename):
	print(clear_terminal.clear())
	print("Done downloading video")
	if (ydl_opts["noplaylist"] == True):
		print(f"file {tcolors.yellow}{filename}{tcolors.clear} was downloaded to your desktop")
	else:
		print(f"playlist {tcolors.yellow}{filename}{tcolors.clear} was downloaded to your desktop")
	input("press enter to quit")
	return

main()