from inputs import get_gamepad
import socket


IP = "192.168.3.1"
PORT = 40
MULTIPLIER = 0.03122    #multiplier to get gamepad value range adjusted to the uC's PWM value range. Here: 32768 (gamepad) / 1023 (PWM ESP8266) = 0.03122
YNOW = 0
RYNOW = 0
YRECENT = 0
RYRECENT = 0
DEADZONE = 350  #minimum value before anything gets sent
STEPSIZE = 80   #minimum value change before it will be sent
THRESHOLD = 50  #if value is between positive and negative threashold, value will be set to zero
SEND = 0


while 1:    
    events = get_gamepad()
    for event in events:
#        print(event.ev_type, event.code, event.state)
        
        CODE = (event.code)
        STATE = (event.state)
        
        if CODE is "ABS_Y":
            YNOW = int(round(STATE * -MULTIPLIER,0))
            print("Left analog stick: ", YNOW)
            if THRESHOLD >= YNOW >= -THRESHOLD:
                YNOW = 0
            if YNOW >= 1023 - THRESHOLD:
                YNOW = 1023
            if YNOW <= -1023 + THRESHOLD:
                YNOW = -1023
            if ((YNOW >= DEADZONE or YNOW <= DEADZONE * -1) and (YNOW >= YRECENT + STEPSIZE or YNOW <= YRECENT - STEPSIZE)) or (YNOW == 0 and YRECENT != 0):
                SEND = 1

        
        if CODE is "ABS_RY":
            RYNOW = int(round(STATE * -0.03122,0))
            print("Right analog stick: ", RYNOW)
            if THRESHOLD >= RYNOW >= -THRESHOLD:
                RYNOW = 0
            if RYNOW >= 1023 - THRESHOLD:
                RYNOW = 1023
            if RYNOW <= -1023 + THRESHOLD:
                RYNOW = -1023
            if ((RYNOW >= DEADZONE or RYNOW <= DEADZONE * -1) and (RYNOW >= RYRECENT + STEPSIZE or RYNOW <= RYRECENT - STEPSIZE)) or (RYNOW == 0 and RYRECENT != 0):
                SEND = 1
        
        
        if SEND is 1:
            DATA = "{}.{}.\n".format(YNOW+1023, RYNOW+1023)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((IP, PORT))
            s.send(DATA.encode())
            s.close
            print("Send:", DATA)

            YRECENT = YNOW
            RYRECENT = RYNOW
            SEND = 0
