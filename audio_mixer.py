import time
import pygame
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"


class AudioMixer():
    """Class to mix audio together with pygame."""

    def __init__(self):
        """Initialise class and load sound files """
        self.file_index = 5
        self.full_volume = 1.0
        self.pause_volume = 0.3
        self.countdown_volume = 0.5
        self._init_mixer()
        self._load_sounds()
        # self.set_loop_event()
        

    def _init_mixer(self):
        """Start pygame mixer."""
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.set_num_channels(16)

    def _load_sounds(self):
        """Load sounds from folder."""
        self.sound_folder = os.path.join(os.path.dirname(__file__), 'sounds')
        self.sound_list = os.listdir(self.sound_folder)
        self.sound_dict = {}
        for file in self.sound_list:
            file_location = os.path.join(self.sound_folder, file)
            first_split = file.split('-')[0]
            if first_split == 'count':
                self.countdown_sound = pygame.mixer.Sound(file_location)
                self.countdown_sound.set_volume(self.countdown_volume)
            else:
                index = int(first_split)
                if index == 1:
                    pygame.mixer.music.load(file_location)
                else:
                    sound = pygame.mixer.Sound(file_location)
                    self.sound_dict[index] = {
                        'name': file, 'sound': sound, 'volume': 0.0}

        self.achievement_folder = os.path.join(os.path.dirname(__file__), 'achievements')
        self.achievement_list = os.listdir(self.achievement_folder)
        self.achievement_dict = {}
        for file in self.achievement_list:
            file_location = os.path.join(self.achievement_folder, file)
            last_split = file.split('-')[0]
            index = int(last_split)
            sound = pygame.mixer.Sound(file_location)
            self.achievement_dict[index] = {
                'name': file, 'sound': sound, 'volume': 0.1}

    def play_achievement(self, index):
        if index > len(self.achievement_dict.keys()):
            index = 6
        pygame.mixer.Channel(15).play(self.achievement_dict[index]['sound'])
        pygame.mixer.Channel(15).set_volume(self.achievement_dict[index]['volume'])

    def set_loop_event(self):
        self.INTERVAL_EVENT = pygame.USEREVENT
        pygame.time.set_timer(self.INTERVAL_EVENT, 30000)
        self.COUNTDOWN_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(self.COUNTDOWN_EVENT, 27000)

    def play(self):
        pygame.mixer.music.play(-1)
        for sound_index in self.sound_dict:
            pygame.mixer.Channel(
                sound_index - 1).play(self.sound_dict[sound_index]['sound'], -1)
            pygame.mixer.Channel(sound_index - 1).set_volume(0.0)
            if sound_index in [2, 3, 4]:
                pygame.mixer.Channel(
                    sound_index - 1).set_volume(self.pause_volume)
                self.sound_dict[sound_index]['volume'] = self.pause_volume

    def increment_file(self):
        self.sound_dict[self.file_index]['volume'] = self.full_volume
        if self.file_index == len(self.sound_dict) + 1:
            return
        else:
            self.file_index += 1
            return

    def update_volumes(self):
        for sound_index in self.sound_dict:
            pygame.mixer.Channel(
                sound_index - 1).set_volume(self.sound_dict[sound_index]['volume'])

    def set_pause_volume(self):
        for sound_index in self.sound_dict:
            if self.sound_dict[sound_index]['volume'] > 0:
                pygame.mixer.Channel(
                    sound_index - 1).set_volume(self.pause_volume)
        pygame.mixer.music.set_volume(self.pause_volume)

    def set_full_volume(self):
        for sound_index in self.sound_dict:
            if self.sound_dict[sound_index]['volume'] > 0:
                pygame.mixer.Channel(
                    sound_index - 1).set_volume(self.full_volume)
        pygame.mixer.music.set_volume(self.full_volume)

    def play_countdown(self):
        pygame.time.set_timer(self.COUNTDOWN_EVENT, 30000)
        pygame.mixer.Channel(14).play(self.countdown_sound)
        pygame.mixer.Channel(14).set_volume(0.5)

def main():
    """Check if all functionality works when running this file from terminal."""
    print('---Testing mixer---')
    am = AudioMixer()
    am.play()

    try:
        while True:
            for event in pygame.event.get():
                if event.type == am.LOOP_EVENT:
                    pygame.mixer.music.play()
                    am.increment_file()
                    am.update_volumes()
    except KeyboardInterrupt:
        pygame.mixer.stop()
        pygame.mixer.quit()


if __name__ == '__main__':
    main()
