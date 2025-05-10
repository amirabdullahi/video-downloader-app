from tkinter import *
from tkinter import filedialog, messagebox
import os
import re
import yt_dlp
import threading

# Global variable for download task
download_task = None
downloading = False

def get_path():
    path = filedialog.askdirectory()
    if path:
        path_label.config(text=path)

def validate_youtube_url(url):
    """Validate if the URL is a proper YouTube URL"""
    youtube_regex = r'(https?://)?(www\.)?(youtube\.com|youtu\.?be)/.+'
    return bool(re.match(youtube_regex, url))

def progress_hook(d):
    """Progress hook for yt-dlp to update the UI"""
    if d['status'] == 'downloading':
        # Calculate percentage
        if 'total_bytes' in d:
            percentage = d['downloaded_bytes'] / d['total_bytes'] * 100
            progress_label.config(text=f"Downloading: {int(percentage)}%")
        elif 'total_bytes_estimate' in d:
            percentage = d['downloaded_bytes'] / d['total_bytes_estimate'] * 100
            progress_label.config(text=f"Downloading: {int(percentage)}% (estimated)")
        else:
            progress_label.config(text=f"Downloaded: {d['downloaded_bytes'] / (1024*1024):.1f} MB")
            
        # Update speed
        if 'speed' in d and d['speed']:
            speed = d['speed'] / (1024*1024)  # Convert to MB/s
            status_var.set(f"Downloading at {speed:.2f} MB/s")
            
        root.update()
        
    elif d['status'] == 'finished':
        progress_label.config(text="Download complete. Processing file...")
        root.update()

def fetch_thumbnail():
    url = url_entry.get().strip()
    if validate_youtube_url(url):
        try:
            # Use yt-dlp to get thumbnail URL
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                thumbnail_url = info.get('thumbnail')
                # For now, just show the thumbnail URL
                status_var.set(f"Thumbnail URL: {thumbnail_url}")
        except Exception as e:
            status_var.set(f"Error fetching thumbnail: {str(e)}")

def cancel_download():
    global downloading
    downloading = False
    status_var.set("Download cancelled")
    cancel_button.config(state=DISABLED)
    download_button.config(state=NORMAL)

def download_thread(video_url, download_path):
    global downloading
    
    try:
        # Configure yt-dlp options
        format_options = {
            "Best Quality Video": "best",
            "720p": "22",
            "Audio Only (MP3)": "bestaudio/best"
        }
        
        ydl_opts = {
            'format': format_options[format_var.get()],
            'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
            'progress_hooks': [progress_hook],
            'quiet': True,
            'no_warnings': True,
            'ignoreerrors': False,
        }
        
        # For audio, add conversion options
        if format_var.get() == "Audio Only (MP3)":
            ydl_opts.update({
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            })
        
        # Handle playlist option
        if playlist_var.get():
            pass  # yt-dlp handles playlists automatically
        else:
            # Extract video ID for single video download
            video_id_match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', video_url)
            if video_id_match:
                video_id = video_id_match.group(1)
                video_url = f"https://www.youtube.com/watch?v={video_id}"
        
        # Get video info first
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            title = info.get('title', 'video')
            status_var.set(f"Preparing to download: {title}")
            root.update()
            
            # Start download if not cancelled
            if downloading:
                status_var.set("Downloading video...")
                progress_label.config(text="Starting download...")
                root.update()
                
                # Download the video
                ydl.download([video_url])
                
                # Download complete if not cancelled
                if downloading:
                    status_var.set("Download Complete!")
                    root.after(0, lambda: messagebox.showinfo("Success", 
                                                             f"Video '{title}' downloaded successfully!"))
        
    except Exception as e:
        error_message = str(e)
        status_var.set(f"Error: {error_message}")
        root.after(0, lambda: messagebox.showerror("Error", f"An error occurred: {error_message}"))
    
    finally:
        # Re-enable download button and disable cancel button
        downloading = False
        root.after(0, lambda: download_button.config(state=NORMAL))
        root.after(0, lambda: cancel_button.config(state=DISABLED))

def download():
    global downloading
    
    # Reset status messages
    status_var.set("")
    progress_label.config(text="")
    
    # Get input values
    video_url = url_entry.get().strip()
    download_path = path_label.cget("text")
    
    # Validate inputs
    if not video_url:
        messagebox.showerror("Error", "Please enter a YouTube URL")
        return
        
    if not validate_youtube_url(video_url):
        messagebox.showerror("Error", "Invalid YouTube URL")
        return
        
    if not download_path:
        messagebox.showerror("Error", "Please select a download location")
        return
    
    # Update UI state
    download_button.config(state=DISABLED)
    cancel_button.config(state=NORMAL)
    status_var.set("Connecting to YouTube...")
    root.update()
    
    # Set downloading flag
    downloading = True
    
    # Start download in a separate thread
    download_thread_obj = threading.Thread(
        target=download_thread, 
        args=(video_url, download_path)
    )
    download_thread_obj.daemon = True
    download_thread_obj.start()


# Create the main window
root = Tk()
root.title("YouTube Video Downloader")
root.geometry("500x550")  # Larger window for new components

# Create a frame for better organization
main_frame = Frame(root, padx=20, pady=20)
main_frame.pack(fill=BOTH, expand=True)

# App title
app_label = Label(main_frame, text="YouTube Video Downloader", fg='blue', font=("Arial", 20))
app_label.pack(pady=10)

# URL input section
url_frame = Frame(main_frame)
url_frame.pack(fill=X, pady=10)
url_label = Label(url_frame, text="Enter YouTube URL:")
url_label.pack(anchor=W)
url_entry = Entry(url_frame, width=50)
url_entry.pack(fill=X, pady=5)

# Format selection section
format_frame = Frame(main_frame)
format_frame.pack(fill=X, pady=10)
format_label = Label(format_frame, text="Download Format:")
format_label.pack(anchor=W)
format_var = StringVar(value="Best Quality Video")
format_menu = OptionMenu(format_frame, format_var, "Best Quality Video", "720p", "Audio Only (MP3)")
format_menu.pack(fill=X)

# Playlist option
playlist_var = BooleanVar(value=False)
playlist_check = Checkbutton(main_frame, text="Download entire playlist", variable=playlist_var)
playlist_check.pack(anchor=W, pady=5)

# Path selection section
path_frame = Frame(main_frame)
path_frame.pack(fill=X, pady=10)
path_label_title = Label(path_frame, text="Download Location:")
path_label_title.pack(anchor=W)
path_label = Label(path_frame, text="", bg="#f0f0f0", width=40, anchor=W, padx=5, pady=5)
path_label.pack(side=LEFT, fill=X, expand=True)
path_button = Button(path_frame, text="Browse", command=get_path)
path_button.pack(side=RIGHT, padx=5)

# Download and cancel buttons
button_frame = Frame(main_frame)
button_frame.pack(fill=X, pady=10)
download_button = Button(button_frame, text="Download Video", command=download, 
                        bg="#4CAF50", fg="white", font=("Arial", 12), padx=10, pady=5)
download_button.pack(side=LEFT, padx=5)
cancel_button = Button(button_frame, text="Cancel", command=cancel_download, 
                      state=DISABLED, padx=10, pady=5)
cancel_button.pack(side=RIGHT, padx=5)

# Status display
status_var = StringVar()
status_label = Label(main_frame, textvariable=status_var, fg="blue")
status_label.pack(pady=5)

# Progress display
progress_label = Label(main_frame, text="", fg="green")
progress_label.pack(pady=5)

# Run the application
root.mainloop()