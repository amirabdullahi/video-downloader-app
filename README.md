A clean, user-friendly desktop application for downloading YouTube videos and audio built with Python and Tkinter.
Features
![Screenshot 2025-05-10 223301-1](https://github.com/user-attachments/assets/c2d7d76c-28f3-485c-8d6d-597bc02aee19)

High-Quality Downloads: Download videos in the highest available quality
Format Options: Choose between video formats or extract audio as MP3
Playlist Support: Download entire YouTube playlists with a single click
Progress Tracking: Real-time download progress and speed information
User-Friendly Interface: Clean, intuitive UI built with Tkinter
Error Handling: Comprehensive error handling and user feedback

Installation
Prerequisites

Python 3.6 or higher
FFmpeg (required for audio extraction)

Setup

Clone the repository:
git clone https://github.com/amirabdullahi/video-downloader-app.git
cd video-downloader-app

Create and activate a virtual environment (recommended):
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate

Install the required dependencies:
pip install -r requirements.txt

Install FFmpeg (if you want to use audio extraction):

Windows: Download FFmpeg and add it to your PATH
macOS: brew install ffmpeg
Linux: sudo apt install ffmpeg



Usage

Run the application:
python downloader.py

Enter a YouTube URL in the input field
Select your desired format (video or audio)
Choose a download location using the "Browse" button
Click "Download Video" to start the download
Monitor the progress in the status area
Your downloaded file will be saved to the selected location

Configuration Options

Best Quality Video: Downloads the highest resolution available
720p: Downloads video in 720p resolution (if available)
Audio Only (MP3): Extracts audio and converts it to MP3 format
Download entire playlist: Enable this option to download all videos in a playlist

Troubleshooting

HTTP Error 400: Try updating yt-dlp with pip install --upgrade yt-dlp
FFmpeg not found: Make sure FFmpeg is properly installed and in your PATH if you're extracting audio
Download fails: Some videos might be restricted or region-locked; try a different video

Requirements

Python 3.6+
yt-dlp
pytube (fallback)
Tkinter (usually included with Python)
FFmpeg (for audio extraction)

Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

Fork the repository
Create your feature branch (git checkout -b feature/amazing-feature)
Commit your changes (git commit -m 'Add some amazing feature')
Push to the branch (git push origin feature/amazing-feature)
Open a Pull Request

License
This project is licensed under the MIT License - see the LICENSE file for details.
Acknowledgments

yt-dlp for the powerful YouTube download engine
pytube for additional YouTube functionality
All contributors and supporters of this project


Note: This application is for personal use only. Please respect YouTube's terms of service and copyright law when downloading content.
