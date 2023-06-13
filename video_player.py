# importing vlc module
import vlc
import os
import time


class VideoPlayer():
    def __init__(self, video_file):

        instance = vlc.Instance()
        self.media_player = instance.media_player_new()
        self.file_location = os.path.join(
            os.path.dirname(__file__), 'videos', video_file)
        media = instance.media_new(self.file_location)
        self.media_player.set_media(media)
        media.parse()

    def start(self):
        self.media_player.play()

    def set_volume(self, volume):
        self.media_player.audio_set_volume(volume)


if __name__ == "__main__":
    video_file = 'video.mp4'
    file_location = os.path.join(
        os.path.dirname(__file__), 'videos', video_file)
    vp = VideoPlayer(file_location)
    vp.start()
