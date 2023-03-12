import cv2 as cv
import mediapipe as mp
import random 


mp_drawing = mp.solutions.drawing_utils 
mp_drawing_styles = mp.solutions.drawing_styles 
mp_hands = mp.solutions.hands 

def getHandMove(hand_landmarks):
    landmarks = hand_landmarks.landmark
    if all([landmarks[i].y < landmarks[i+3].y for i in range(9 , 20 , 4)]):
        return 1 #piedra
    elif landmarks[13].y < landmarks[16].y and landmarks[17].y < landmarks[20].y:
        return 2 #tijeras
    else:
        return 3 #papel

vid = cv.VideoCapture(1)

p1_move = None
p2_move = random.randint(1,3)

gameText = ''
clock = 0
success = True

with mp_hands.Hands(model_complexity = 8, min_detection_confidence=0.5,min_tracking_confidence=0.5) as hands:
    while True:
        ret, frame = vid.read()
        if not ret or frame is None: break
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        result = hands.process(frame)
        frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)
        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS, mp_drawing_styles.get_default_hand_landmarks_style(), mp_drawing_styles.get_default_hand_connections_style())   
        frame = cv.flip(frame, 1)
        if 0<=clock<20:
            success = True
            gameText = 'ready?'
        elif clock<30: 
            gameText = '..3'
        elif clock<40:
            gameText = '..2'
        elif clock<50:
            gameText = '..1'
        elif clock<60:
            gameText = 'GO!'
        elif clock==60:
            hls = result.multi_hand_landmarks
            if hls and len(hls)==1:
                p1_move = getHandMove(hls[0])
            else:
                success = False
        elif clock<100:
            if success:
                gameText = f"player 1: {p1_move}, player 2: {p2_move}"
                if p1_move==p2_move:
                    gameText = 'Is a tie'
                elif p1_move==1 and p2_move==2:
                    gameText = 'Player 1 wins'
                elif p1_move==2 and p2_move==3:
                    gameText = 'Player 1 wins'
                elif p1_move==3 and p2_move==1:
                    gameText = 'player 1 wins'
                else:
                    gameText = 'Player 2 wins'
            
                
            else:
                gameText = 'Try again'

        cv.putText(frame, f"Clock: {clock}", (50, 50), cv.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 2, cv.LINE_AA)
        cv.putText(frame, gameText, (50, 50), cv.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 2, cv.LINE_AA)
        clock = (clock+1)%100
        cv.imshow('frame', frame)
        if cv.waitKey(1) & 0xFF == ord('q'): break
vid.release()
cv.destroyAllWindows()
