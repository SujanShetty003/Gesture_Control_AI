import cv2
import mediapipe as mp
import pyautogui

mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic
mp_hands = mp.solutions.hands
cap = cv2.VideoCapture(0)
tipIds = [4, 8, 12, 16, 20]
game_started = 1
charac_pos = [0, 1, 0]
index_pos = 1
fixedx = None
fixedy = None
rec = None

with mp_hands.Hands(min_detection_confidence=0.3, min_tracking_confidence=0.3) as hands:
    with mp_holistic.Holistic(min_detection_confidence=0.3, min_tracking_confidence=0.3) as holistic:
        while True:
            success, frame = cap.read()
            if not success:
                print("Failed to capture frame from the webcam. Check your camera.")
                continue

            # Flip and resize the frame
            frame = cv2.flip(frame, 1)
            frame = cv2.resize(frame, (440, 330))
            height, width, _ = frame.shape

            # Convert the frame to RGB
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results_holistic = holistic.process(img)
            results_hands = hands.process(img)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

            # Debug: Check if pose and hands are detected
            print("Pose landmarks:", results_holistic.pose_landmarks)
            print("Hand landmarks:", results_hands.multi_hand_landmarks)
            print("Handedness:", results_hands.multi_handedness)

            width_hf = int(width / 2)
            height_hf = int(height / 2)

            # Extracting Shoulder Landmarks
            if results_holistic.pose_landmarks:
                try:
                    right_x = int(results_holistic.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_SHOULDER].x * width) - 7
                    right_y = int(results_holistic.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_SHOULDER].y * height)
                    left_x = int(results_holistic.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_SHOULDER].x * width) + 7
                    left_y = int(results_holistic.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_SHOULDER].y * height)
                    mid_x = left_x + int(abs(right_x - left_x) / 2)
                    mid_y = int(abs(right_y + left_y) / 2)

                    # Debug: Shoulder positions
                    print("Right Shoulder:", right_x, right_y)
                    print("Left Shoulder:", left_x, left_y)
                    print("Midpoint:", mid_x, mid_y)

                    if rec is not None:
                        if right_x < width_hf and index_pos > 0 and charac_pos[index_pos - 1] == 0:
                            pyautogui.press('left')
                        if left_x > width_hf and index_pos < 2 and charac_pos[index_pos + 1] == 0:
                            pyautogui.press('right')
                except Exception as e:
                    print("Error in shoulder detection:", e)

            hand_cor_list_right = []
            hand_cor_list_left = []
            fingers_right = []
            fingers_left = []
            try:
                if results_hands.multi_handedness:
                    hand_type1 = results_hands.multi_handedness[0].classification[0].label
                    if len(results_hands.multi_handedness) > 1:
                        hand_type2 = results_hands.multi_handedness[1].classification[0].label
                    else:
                        hand_type2 = None

                    for hand_no, hand_landmarks in enumerate(results_hands.multi_hand_landmarks):
                        if hand_no == 0:
                            if hand_type1 == 'Left':
                                for id, lm in enumerate(hand_landmarks.landmark):
                                    cx, cy = int(lm.x * width), int(lm.y * height)
                                    hand_cor_list_left.append([id, cx, cy])
                            elif hand_type1 == 'Right':
                                for id, lm in enumerate(hand_landmarks.landmark):
                                    cx, cy = int(lm.x * width), int(lm.y * height)
                                    hand_cor_list_right.append([id, cx, cy])
                        if hand_no == 1 and hand_type2:
                            if hand_type2 == 'Left':
                                for id, lm in enumerate(hand_landmarks.landmark):
                                    cx, cy = int(lm.x * width), int(lm.y * height)
                                    hand_cor_list_left.append([id, cx, cy])
                            elif hand_type2 == 'Right':
                                for id, lm in enumerate(hand_landmarks.landmark):
                                    cx, cy = int(lm.x * width), int(lm.y * height)
                                    hand_cor_list_right.append([id, cx, cy])

                # Process fingers for the right hand
                if hand_cor_list_right:
                    if hand_cor_list_right[tipIds[0]][1] < hand_cor_list_right[tipIds[0] - 1][1]:
                        fingers_right.append(1)
                    else:
                        fingers_right.append(0)
                    for id in range(1, 5):
                        if hand_cor_list_right[tipIds[id]][2] < hand_cor_list_right[tipIds[id] - 2][2]:
                            fingers_right.append(1)
                        else:
                            fingers_right.append(0)

                # Process fingers for the left hand
                if hand_cor_list_left:
                    if hand_cor_list_left[tipIds[0]][1] > hand_cor_list_left[tipIds[0] - 1][1]:
                        fingers_left.append(1)
                    else:
                        fingers_left.append(0)
                    for id in range(1, 5):
                        if hand_cor_list_left[tipIds[id]][2] < hand_cor_list_left[tipIds[id] - 2][2]:
                            fingers_left.append(1)
                        else:
                            fingers_left.append(0)

                # Debug: Fingers detection
                print("Fingers Right:", fingers_right)
                print("Fingers Left:", fingers_left)
            except Exception as e:
                print("Error in hand processing:", e)

            # Gesture-based actions
            if fingers_right.count(1) == 2 and fingers_left.count(1) == 2 and fingers_right[1] == 1 and fingers_right[2] == 1 and fingers_left[1] == 1 and fingers_left[2] == 1:
                fixedx = left_x + int(abs(right_x - left_x) / 2)
                fixedy = int(abs(right_y + left_y) / 2)
                rec = 35
                pyautogui.press('space')

            if fixedy is not None:
                if (mid_y - fixedy) <= -24:
                    pyautogui.press('up')
                elif (mid_y - fixedy) >= 40:
                    pyautogui.press('down')

            # Draw landmarks for visualization
            if results_hands.multi_hand_landmarks:
                for hand_landmarks in results_hands.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            if results_holistic.pose_landmarks:
                mp_drawing.draw_landmarks(img, results_holistic.pose_landmarks, mp_holistic.POSE_CONNECTIONS)

            # Draw UI
            center_arrow = 30
            cv2.circle(img, (width_hf, height_hf), 2, (0, 255, 255), 2)
            cv2.line(img, (width_hf, height_hf - center_arrow), (width_hf, height_hf + center_arrow), (0, 255, 0), 2)
            cv2.line(img, (width_hf - center_arrow, height_hf), (width_hf + center_arrow, height_hf), (0, 255, 0), 2)
            cv2.imshow('Subway Surfers', img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

cap.release()
cv2.destroyAllWindows()
