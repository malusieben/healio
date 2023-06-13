import time
import cwiid


class WiiBoard():
    def __init__(self):
        pass
    
    def __delete__(self):
        if self.balance_board:
            self.balance_board.close()

    def connect(self):
        print('Press the red sync button on the back of the Wii Balance Board...')
        time.sleep(1)
        self.balance_board = None
        try:
            self.balance_board = cwiid.Wiimote()
            self.balance_board.rpt_mode = cwiid.RPT_BALANCE
            print('Wii Balance Board connected!')
        except RuntimeError:
            print("Failed to connect to Wii Balance Board")
            quit()
        balance_calibration = self.balance_board.get_balance_cal()
        self.right_top_cal = balance_calibration[0][0]
        self.right_bottom_cal = balance_calibration[1][0]
        self.left_top_cal = balance_calibration[2][0]
        self.left_bottom_cal = balance_calibration[3][0]

    def get_state(self):
        return self.balance_board.state['balance']

    def get_weight(self):
        state = self.balance_board.state['balance']
        return state['right_top'] + state['right_bottom'] + state['left_top'] + state['left_bottom']

    def get_balance(self):
        state = self.balance_board.state['balance']
        right = state['right_top'] - self.right_top_cal + state['right_bottom'] - self.right_bottom_cal
        if right < 0:
            right = 0
        left = state['left_top'] - self.left_top_cal + state['left_bottom'] - self.left_bottom_cal 
        if left < 0:
            left = 0
        if (left + right) == 0:
            balance = 0.5
        else:
            balance = right / (left + right)  
        return balance