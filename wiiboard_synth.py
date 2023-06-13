
import time
import pygame

from audio_mixer import AudioMixer
from data_handler import DataHandler
from wiiboard import WiiBoard
from custom_timer import Timer
from video_player import VideoPlayer


class WiiBoardSynth():
    def __init__(self):
        print('Setting up WiiBoard Synth')
        # ALLE ONDERDELEN AANROEPEN
        self.audio_mixer = AudioMixer()
        self.wii_board = WiiBoard()
        self.data_handler = DataHandler('data_malu.xlsx')
        self.video_player = VideoPlayer('video_v2.mp4')
        self.timer = Timer()
        # INSTELLEN PARAMETERS
        self.balance_threshold = 0.35
        self.interval_index = 0
        self.pause = True
        self.video_volume = 50
        # DATA OPHALEN
        self.intervals = self.data_handler.get_averages()

    def passed_interval(self, duration):
        # CHECK OF VOORBIJ LAATSTE INTERVAL
        if self.interval_index == (len(self.intervals)):
            return False # NIET VOORBIJ INTERVAL
        # CHECK OF ER INTERVALS ZIJN
        if len(self.intervals) > 0:
            # CHECK OF HUIDIGE TIJD VERDER DAN INTERVAL
            if duration > self.intervals[self.interval_index]:
                if self.interval_index < (len(self.intervals)):
                    print('Passed interval {} with duration {}.'.format(
                        self.interval_index, duration))
                    self.interval_index += 1 # NEEM HET VOLGENDE INTERVAL VOOR CHECK
                    return True # WE ZIJN VOORBIJ INTERVAL
                else:
                    return False # NIET VOORBIJ INTERVAL
            else:
                return False # NIET VOORBIJ INTERVAL

    def in_balance(self):
        balance = self.wii_board.get_balance()
        if self.balance_threshold < balance < 1 - self.balance_threshold:
            return False # NIET IN BALANS
        else:
            return True # IN BALANS

    def start(self):
        self.audio_mixer.play() # GELUID STARTEN
        duration = 0
        achievement_index = 1 # HOUDT BIJ WELK ACHIEVEMENT
        try:
            while True:
                # EXERCISE LOOP
                self.video_player.set_volume(self.video_volume)
                for event in pygame.event.get():
                    if event.type == self.audio_mixer.INTERVAL_EVENT: # TRUE TIME - SWITCH BREAK/EXERCISE
                        if self.pause: # ALS JE PAUZEERT...
                            self.pause = False # STOP MET PAUZEREN
                            try:
                                self.timer.resume()
                            except ValueError:
                                self.timer.start()
                            if not self.in_balance():
                                break    
                            self.audio_mixer.set_full_volume()
                        else: # ALS JE NIET PAUZEERT
                            self.pause = True # GA PAUZEREN
                            self.timer.pause()
                            self.audio_mixer.set_pause_volume()
                    if event.type == self.audio_mixer.COUNTDOWN_EVENT: # COUNTDOWN TIME - PLAY SOUND
                        self.audio_mixer.play_countdown()

                if not self.pause: # TIJDENS EXERCISE
                    duration = self.timer.get() # HOE LANG BEZIG
                    if not self.in_balance(): # IN BALANS?
                        break
                    if self.passed_interval(duration): # LANGS INTERVAL?
                        self.audio_mixer.increment_file()
                        self.audio_mixer.update_volumes()
                        self.audio_mixer.play_achievement(achievement_index)
                        achievement_index += 1
                time.sleep(0.0001) # PREVENT MENTAL BREAKDOWN FOR PC
        except KeyboardInterrupt:
            pass
        finally: # ALS STOP
            try:
                duration = self.timer.get() # TIJD OPHALEN
                if duration > 2.0:
                    self.data_handler.save_time(duration) # TIJD OPSLAAN
                    print('Time was {}'.format(duration)) # TIJD LATEN ZIEN
                else:
                    print('Time was too short')
            except ValueError:
                print('Time was zero')
            pygame.mixer.stop()
            pygame.mixer.quit()

    def startup(self):
        self.wii_board.connect()
        self.video_player.start()
        self.audio_mixer.set_loop_event()


def main():
    wbs = WiiBoardSynth()
    wbs.startup()
    wbs.start()


if __name__ == '__main__':
    main()
