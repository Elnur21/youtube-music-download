import flet
from flet import IconButton, Page, Row, TextField, icons, Text, Column, ProgressBar
import yt_dlp


def main(page: Page):
    page.window_bgcolor = "blue"
    page.window_width = 300.00
    page.window_height = 720.00
    page.title = "YouTube Downloader"
    page.vertical_alignment = "center"

    status_text = Text(value="", color="white", size=16)
    progress = ProgressBar(width=200, value=0)

    def show_status(message, success=True):
        """Update the status message with success or error."""
        status_text.value = message
        status_text.color = "green" if success else "red"
        page.update()

    def install_video(e):
        """Download video using yt-dlp."""
        try:
            show_status("Downloading video...")
            ydl_opts = {
                "format": "bestvideo+bestaudio/best",
                "outtmpl": "downloads/%(title)s.%(ext)s", 
                "progress_hooks": [on_download_progress],
                "noplaylist": True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([link.value])
            show_status("Video downloaded successfully!", success=True)
        except Exception as ex:
            show_status(f"Error: {str(ex)}", success=False)

    def install_audio(e):
        """Download audio as MP3 using yt-dlp."""
        try:
            show_status("Downloading audio...")
            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl": "downloads/%(title)s.%(ext)s",  
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }
                ],
                "progress_hooks": [on_download_progress],
                "noplaylist": True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([link.value])
            show_status("Audio downloaded successfully!", success=True)
        except Exception as ex:
            show_status(f"Error: {str(ex)}", success=False)

    def on_download_progress(d):
        """Update the progress bar during download."""
        if d["status"] == "downloading":
            percentage = d.get("_percent_str", "0%").strip("%")
            try:
                progress.value = float(percentage) / 100  
                page.update()
            except ValueError:
                show_status("Error parsing progress value", success=False)

    link = TextField(value="", text_align="center", width=200, hint_text="Enter YouTube link")

    page.add(
        Column(
            [
                Text(value="Enter YouTube link:", color="white", size=18),
                link,
                Row(
                    [
                        IconButton(icon=icons.VIDEO_FILE, on_click=install_video, tooltip="Download Video"),
                        IconButton(icon=icons.AUDIO_FILE, on_click=install_audio, tooltip="Download Audio"),
                    ],
                    alignment="center",
                ),
                progress,
                status_text,
            ],
            alignment="center",
        )
    )


flet.app(target=main)
