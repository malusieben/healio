from datetime import datetime

class Timer():
    """
    timer.start() - should start the timer
    timer.pause() - should pause the timer
    timer.resume() - should resume the timer
    timer.get() - should return the current time
    """

    def __init__(self):
        print('Initializing timer')
        self.timestarted = None
        self.timepaused = None
        self.paused = False

    def start(self):
        """ Starts an internal timer by recording the current time """
        print("Starting timer")
        self.timestarted = datetime.now()

    def pause(self):
        """ Pauses the timer """
        if self.timestarted is None:
            raise ValueError("Timer not started")
        if self.paused:
            raise ValueError("Timer is already paused")
        print('Pausing timer')
        self.timepaused = datetime.now()
        self.paused = True

    def resume(self):
        """ Resumes the timer by adding the pause time to the start time """
        if self.timestarted is None:
            raise ValueError("Timer not started")
        if not self.paused:
            raise ValueError("Timer is not paused")
        print('Resuming timer')
        pausetime = datetime.now() - self.timepaused
        self.timestarted = self.timestarted + pausetime
        self.paused = False

    def get(self):
        """ Returns a timedelta object showing the amount of time
            elapsed since the start time, less any pauses """
        if self.timestarted is None:
            raise ValueError("Timer not started")
        if self.paused:
            time = self.timepaused - self.timestarted
            return time.total_seconds()
        else:
            time = datetime.now() - self.timestarted
            return time.total_seconds()
