import os
import cv2
from multiprocessing import Process


class VideoPlayer():
    def __init__(self, video_file):
        self.file_location = os.path.join(
            os.path.dirname(__file__), 'videos', video_file)
        self.data = None
        self.kill = False

    def start_local_video(self):
        path = self.file_location
        cap = cv2.VideoCapture(path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
        cv2.setWindowProperty(
            'frame', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        while (not self.kill):
            ret, frame = cap.read()
            if ret:
                cv2.imshow('frame', frame)
                if cv2.waitKey(int(1000 / fps)) & 0xFF == ord('q'):
                    break
            else:
                break
        cap.release()
        cv2.destroyAllWindows()

    def start(self):
        print('Starting video')
        self.process = Process(target=self.start_local_video)
        self.process.start()

    def stop(self):
        self.process.kill()
        self.process.join()