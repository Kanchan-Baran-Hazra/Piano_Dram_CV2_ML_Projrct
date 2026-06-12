
import os
import cv2
import mediapipe as mp
import pygame
import time

# -----------------------------
# Initialize Audio
# -----------------------------
pygame.mixer.init()

notes1 = {
    "C": pygame.mixer.Sound(os.path.join('Assets','piano-mp3','C1.mp3')),
    "D": pygame.mixer.Sound(os.path.join('Assets','piano-mp3','C2.mp3')),
    "E": pygame.mixer.Sound(os.path.join('Assets','piano-mp3','C3.mp3')),
    "F": pygame.mixer.Sound(os.path.join('Assets','piano-mp3','C4.mp3')),
    "G": pygame.mixer.Sound(os.path.join('Assets','piano-mp3','C5.mp3')),
    "A": pygame.mixer.Sound(os.path.join('Assets','piano-mp3','C6.mp3')),
    "B": pygame.mixer.Sound(os.path.join('Assets','piano-mp3','C7.mp3')),
    "C#": pygame.mixer.Sound(os.path.join('Assets','piano-mp3','D1.mp3')),
    "D#": pygame.mixer.Sound(os.path.join('Assets','piano-mp3','D2.mp3')),
    "F#": pygame.mixer.Sound(os.path.join('Assets','piano-mp3','D3.mp3')),
    "G#": pygame.mixer.Sound(os.path.join('Assets','piano-mp3','D4.mp3')),
    "A#": pygame.mixer.Sound(os.path.join('Assets','piano-mp3','D5.mp3')),
}

notes2 = {
    "C": pygame.mixer.Sound(os.path.join('Assets','dram_sound','a1.wav')),
    "D": pygame.mixer.Sound(os.path.join('Assets','dram_sound','a2.wav')),
    "E": pygame.mixer.Sound(os.path.join('Assets','dram_sound','a3.wav')),
    "F": pygame.mixer.Sound(os.path.join('Assets','dram_sound','a4.wav')),
    "G": pygame.mixer.Sound(os.path.join('Assets','dram_sound','a5.wav')),
    "A": pygame.mixer.Sound(os.path.join('Assets','dram_sound','a6.wav')),
    "B": pygame.mixer.Sound(os.path.join('Assets','dram_sound','a7.wav')),
    "C#": pygame.mixer.Sound(os.path.join('Assets','dram_sound','a8.wav')),
    "D#": pygame.mixer.Sound(os.path.join('Assets','dram_sound','a9.wav')),
    "F#": pygame.mixer.Sound(os.path.join('Assets','dram_sound','a10.wav')),
    "G#": pygame.mixer.Sound(os.path.join('Assets','dram_sound','a11.wav')),
    "A#": pygame.mixer.Sound(os.path.join('Assets','dram_sound','a12.wav')),
}

notes=notes1

# -----------------------------
# Initialize MediaPipe
# -----------------------------
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils



hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# -----------------------------
# Camera
# -----------------------------
cap = cv2.VideoCapture(0)

# Prevent continuous replay
last_note = None
last_time = 0
cooldown = 0.3

previous_y = None
tap_threshold = 15

while True:

    success, frame = cap.read()
    # current_note = None

    if not success:
        print("Camera access denied..!!")
        break

    frame = cv2.flip(frame, 1)

    height, width, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = hands.process(rgb)
    # print(result)

    # piano_top = height - 300
    # piano_bottom = height - 150

    # -----------------------------
    # Draw Piano Keys
    # -----------------------------
    # key_width = width // 8
    white_notes = ["C", "D", "E", "F", "G", "A", "B"]

    white_width = width // 7
    piano_top = 250
    piano_bottom = 450

    # keys = {
    #     "C": (0, key_width),
    #     "D": (key_width, key_width * 2),
    #     "E": (key_width * 2, key_width * 3),
    #     "F": (key_width * 3, key_width*4),
    #     "G": (key_width * 4, key_width*5),
    #     "H": (key_width * 5, key_width*6),
    #     "I": (key_width * 6, key_width*7),
    #     "J":(key_width*7,width),
    # }

    white_key_positions={
        "C":(0,white_width,piano_top,piano_bottom),
        "D":(white_width,white_width*2,piano_top,piano_bottom),
        "E":(white_width*2,white_width*3,piano_top,piano_bottom),
        "F":(white_width*3,white_width*4,piano_top,piano_bottom),
        "G":(white_width*4,white_width*5,piano_top,piano_bottom),
        "A":(white_width*5,white_width*6,piano_top,piano_bottom),
        "B":(white_width*6,width,piano_top,piano_bottom),
    }
    
    # print(current_note)
    for i, note in enumerate(white_notes):

        x1 = i * white_width
        x2 = x1 + white_width
    
        cv2.rectangle(
            frame,
            (x1, piano_top),
            (x2, piano_bottom),
            (255,255,255),
            2
        )
    
        cv2.putText(
            frame,
            note,
            (x1 + 20, piano_bottom - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )
    
    black_keys = [
        ("C#", 0),
        ("D#", 1),
        ("F#", 3),
        ("G#", 4),
        ("A#", 5),
    ]

    black_width = white_width // 2
    black_height = 120

    black_key_positions = {}

    for note, pos in black_keys:
    
        center_x = (pos + 1) * white_width
    
        x1 = center_x - black_width // 2
        x2 = center_x + black_width // 2
    
        cv2.rectangle(
            frame,
            (x1, piano_top),
            (x2, piano_top + black_height),
            (1,1,2),
            -1
        )

        black_key_positions[note] = (
            x1,
            x2,
            piano_top,
            piano_top + black_height
        )
    
        cv2.putText(
            frame,
            note,
            (x1 + 5, piano_top + 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            1
        )

    # -----------------------------
    # Hand Detection
    # -----------------------------
    if result.multi_hand_landmarks:

        for hand_landmarks, handedness in zip(
            result.multi_hand_landmarks,
            result.multi_handedness
        ):

            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            
            hand_label = handedness.classification[0].label

            print(hand_label)

            if hand_label=='Left':

                index_up  = hand_landmarks.landmark[8].y  < hand_landmarks.landmark[6].y
                middle_up = hand_landmarks.landmark[12].y < hand_landmarks.landmark[10].y
                ring_up   = hand_landmarks.landmark[16].y < hand_landmarks.landmark[14].y
                pinky_up  = hand_landmarks.landmark[20].y < hand_landmarks.landmark[18].y
    
                open_palm = (
                    index_up and
                    middle_up and
                    ring_up and
                    pinky_up
                )

            else:
                finger_tips = [8,12,16,20]
                for finger_id in finger_tips:
                # Index fingertip = landmark 8
                    tip = hand_landmarks.landmark[finger_id]
                    # print(f'------{tip}-----')
    
                    
                    
                    print(open_palm)
    
                    if open_palm:
                        notes=notes1
                    else:
                        notes=notes2
        
                    x = int(tip.x * width)
                    y = int(tip.y * height)
        
                    if previous_y is not None:
                        velocity = y - previous_y
                    else:
                        velocity = 0
                    previous_y = y
        
                    cv2.circle(frame, (x, y), 7, (0, 0, 255), -1)
        
        
                    current_note = None
                    # Check black keys first
                    for note, (x1,x2,y1,y2) in black_key_positions.items():
                    
                        if x1 <= x <= x2 and y1 <= y <= y2:
                            current_note = note
                            break
                    
                    # Then white keys
                    if current_note is None:
                    
                        for note, (x1,x2,y1,y2) in white_key_positions.items():
                    
                            if x1 <= x <= x2 and y1 <= y <= y2:
                                current_note = note
                                break
                    current_time = time.time()
                    if (
                        current_note
                        and (
                            current_note != last_note
                            or current_time - last_time > cooldown
                        ) and velocity > tap_threshold
                    ):
                        notes[current_note].play()
                        last_note = current_note
                        last_time = current_time
                        print("Playing:", current_note)
        
                    is_black=False
                    for note,pos in black_keys:
        
                        center_x = (pos + 1) * white_width
            
                        x1 = center_x - black_width // 2
                        x2 = center_x + black_width // 2
        
                        if current_note==note:
                            is_black=True
                            cv2.rectangle(
                                frame,
                                (x1, piano_top),
                                (x2, piano_top+black_height),
                                (0,0,255),
                                4
                            )
        
                    if not is_black:
                        for i, note in enumerate(white_notes):
            
                            x1 = i * white_width
                            x2 = x1 + white_width
            
                            if current_note==note:
                                cv2.rectangle(
                                    frame,
                                    (x1, piano_top),
                                    (x2, piano_bottom),
                                    (50, 205, 50),
                                    9
                                )

    cv2.imshow("Air Piano", frame)

    key = cv2.waitKey(1)

    if key == 27:  # ESC
        break

cap.release()
cv2.destroyAllWindows()

























# import os
# import cv2
# import mediapipe as mp
# import pygame
# import time

# # -----------------------------
# # Initialize Audio
# # -----------------------------
# pygame.mixer.init()

# notes = {
#     "C": pygame.mixer.Sound(os.path.join('piano-mp3','piano-mp3','C1.mp3')),
#     "D": pygame.mixer.Sound(os.path.join('piano-mp3','piano-mp3','C2.mp3')),
#     "E": pygame.mixer.Sound(os.path.join('piano-mp3','piano-mp3','C3.mp3')),
#     "F": pygame.mixer.Sound(os.path.join('piano-mp3','piano-mp3','C4.mp3')),
#     "G": pygame.mixer.Sound(os.path.join('piano-mp3','piano-mp3','C5.mp3')),
#     "H": pygame.mixer.Sound(os.path.join('piano-mp3','piano-mp3','C6.mp3')),
#     "I": pygame.mixer.Sound(os.path.join('piano-mp3','piano-mp3','C7.mp3')),
#     "J": pygame.mixer.Sound(os.path.join('piano-mp3','piano-mp3','C8.mp3')),
# }

# # -----------------------------
# # Initialize MediaPipe
# # -----------------------------
# mp_hands = mp.solutions.hands
# mp_draw = mp.solutions.drawing_utils



# hands = mp_hands.Hands(
#     static_image_mode=False,
#     max_num_hands=1,
#     min_detection_confidence=0.7,
#     min_tracking_confidence=0.7
# )

# # -----------------------------
# # Camera
# # -----------------------------
# cap = cv2.VideoCapture(0)

# # Prevent continuous replay
# last_note = None
# last_time = 0
# cooldown = 0.3

# while True:

#     success, frame = cap.read()

#     if not success:
#         print("Camera access denied..!!")
#         break

#     frame = cv2.flip(frame, 1)

#     height, width, _ = frame.shape

#     rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

#     result = hands.process(rgb)
#     # print(result)

#     # piano_top = height - 300
#     # piano_bottom = height - 150

#     # -----------------------------
#     # Draw Piano Keys
#     # -----------------------------
#     key_width = width // 8

#     keys = {
#         "C": (0, key_width),
#         "D": (key_width, key_width * 2),
#         "E": (key_width * 2, key_width * 3),
#         "F": (key_width * 3, key_width*4),
#         "G": (key_width * 4, key_width*5),
#         "H": (key_width * 5, key_width*6),
#         "I": (key_width * 6, key_width*7),
#         "J":(key_width*7,width),
#     }
    

#     for note, (x1, x2) in keys.items():
#         # print(note)
#         # print(x1,x2)

#         cv2.rectangle(
#             frame,
#             (x1, height - 150),
#             (x2, height),
#             (255,255,255),
#             10
#         )

#         cv2.putText(
#             frame,
#             note,
#             (x1 + 40, height - 50),
#             cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,
#             1,
#             (0,255,255),
#             2
#         )

#     # -----------------------------
#     # Hand Detection
#     # -----------------------------
#     if result.multi_hand_landmarks:

#         for hand in result.multi_hand_landmarks:

#             mp_draw.draw_landmarks(
#                 frame,
#                 hand,
#                 mp_hands.HAND_CONNECTIONS
#             )

#             # Index fingertip = landmark 8
#             tip = hand.landmark[8]
#             # print(f'------{tip}-----')

#             x = int(tip.x * width)
#             y = int(tip.y * height)

#             cv2.circle(frame, (x, y), 7, (0, 0, 255), -1)

#             # Only trigger when finger enters key area
#             if y > height - 150:

#                 current_note = None

#                 for note, (x1, x2) in keys.items():

#                     if x1 <= x < x2:
#                         current_note = note
#                         break

#                 current_time = time.time()

#                 if (
#                     current_note
#                     and (
#                         current_note != last_note
#                         or current_time - last_time > cooldown
#                     )
#                 ):
#                     notes[current_note].play()

#                     last_note = current_note
#                     last_time = current_time

#                     print("Playing:", current_note)

#     cv2.imshow("Air Piano", frame)

#     key = cv2.waitKey(1)

#     if key == 27:  # ESC
#         break

# cap.release()
# cv2.destroyAllWindows()







































# import pygame
# import os

# pygame.init()
# pygame.mixer.init()

# # Load sounds
# sounds = {
#     pygame.K_a: pygame.mixer.Sound(os.path.join('piano-mp3','piano-mp3','C1.mp3')),
#     pygame.K_s: pygame.mixer.Sound(os.path.join('piano-mp3','piano-mp3','C2.mp3')),
#     pygame.K_d: pygame.mixer.Sound(os.path.join('piano-mp3','piano-mp3','C3.mp3')),
#     pygame.K_f: pygame.mixer.Sound(os.path.join('piano-mp3','piano-mp3','C4.mp3')),
# }

# screen = pygame.display.set_mode((500, 200))
# pygame.display.set_caption("Simple Piano")

# running = True

# while running:
#     for event in pygame.event.get():
#         print(event.type)
#         if event.type == pygame.QUIT:
#             running = False

#         if event.type == pygame.KEYDOWN:
#             if event.key in sounds:
#                 sounds[event.key].play()

# pygame.quit()