import cv2
import time
import pyautogui
import mediapipe as mp
import numpy as np
from math import acos, degrees

def calculateRange(num, Range=50):
    """
    Takes a list num containing two numbers [x, y] as input and generates a list of numbers for each of the two numbers, x and y, with a specified range.
    """
    x = num[0]
    y = num[1]

    # Calculate range of numbers around x and y
    previous_numbers_x = list(range(x - Range, x))
    following_numbers_x = list(range(x + 1, x + (Range + 1)))
    range_x = previous_numbers_x + [x] + following_numbers_x

    previous_numbers_y = list(range(y - Range, y))
    following_numbers_y = list(range(y + 1, y + (Range + 1)))
    range_y = previous_numbers_y + [y] + following_numbers_y

    return [range_x, range_y]

def matches_lists(list1, list2):
    """
    Return True if matches any element in the two lists.
    """
    # Check if any element in list1 matches with any element in list2
    for element in list1:
        if element in list2:
            return True
    return False

def palm_centroid(coordinates_list):
    """
    Calculates the centroid of a list of coordinates.
    """
    # Convert list of coordinates to numpy array
    coordinates = np.array(coordinates_list)
    # Compute centroid as mean of coordinates along each axis
    centroid = np.mean(coordinates, axis=0)
    # Convert centroid coordinates to integer values
    centroid = int(centroid[0]), int(centroid[1])
    return centroid

def init_control_cursor():
    # Setup mediapipe modules for hand tracking
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_hands = mp.solutions.hands

    # Initialize video capture from default camera (0)
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    # Define landmark indices for thumb, fingers, and palm points
    thumb_points = [1, 2, 4]
    palm_points = [0, 1, 2, 5, 9, 13, 17]
    fingertips_points = [8, 12, 16, 20]
    finger_base_points = [6, 10, 14, 18]

    # Define colors for drawing on screen
    GREEN = (48, 255, 48)
    BLUE = (192, 101, 21)
    YELLOW = (0, 204, 255)
    PURPLE = (128, 64, 128)
    PEACH = (180, 229, 255)

    # Start hand tracking process
    with mp_hands.Hands(
        model_complexity=1,
        max_num_hands=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:

        while True:
            # Capture frame-by-frame from camera
            ret, frame = cap.read()
            if not ret:
                break

            # Flip frame horizontally for natural hand movement mirroring
            frame = cv2.flip(frame, 1)
            height, width, _ = frame.shape

            # Convert frame to RGB for mediapipe processing
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process the frame to detect hands
            results = hands.process(frame_rgb)
            fingers_counter = "_"
            thickness = [2, 2, 2, 2, 2]

            # Initialize lists for storing coordinates of hand landmarks
            coordinates_centroid = []
            coordinates_thumb = []
            coordinates_palm = []
            coordinates_ft = []
            coordinates_fb = []

            coord = ["", ""]
            
            # If hands are detected in the frame, extract landmark coordinates
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    for index in thumb_points:
                        x = int(hand_landmarks.landmark[index].x * width)
                        y = int(hand_landmarks.landmark[index].y * height)
                        coordinates_thumb.append([x, y])

                    for index in palm_points:
                        x = int(hand_landmarks.landmark[index].x * width)
                        y = int(hand_landmarks.landmark[index].y * height)
                        coordinates_palm.append([x, y])

                    for index in fingertips_points:
                        x = int(hand_landmarks.landmark[index].x * width)
                        y = int(hand_landmarks.landmark[index].y * height)
                        coordinates_ft.append([x, y])

                    for index in finger_base_points:
                        x = int(hand_landmarks.landmark[index].x * width)
                        y = int(hand_landmarks.landmark[index].y * height)
                        coordinates_fb.append([x, y])

                    # Calculate angles and distances for gesture recognition
                    p1 = np.array(coordinates_thumb[0])
                    p2 = np.array(coordinates_thumb[1])
                    p3 = np.array(coordinates_thumb[2])

                    l1 = np.linalg.norm(p2 - p3)
                    l2 = np.linalg.norm(p1 - p3)
                    l3 = np.linalg.norm(p1 - p2)

                    angle = degrees(acos((l1**2 + l3**2 - l2**2) / (2 * l1 * l3)))
                    thumb_finger = np.array(False)
                    if angle > 150:
                        thumb_finger = np.array(True)

                    # Calculate centroid of palm coordinates
                    nx, ny = palm_centroid(coordinates_palm)
                    cv2.circle(frame, (nx, ny), 3, (0, 255, 0), 2)
                    coordinates_centroid = np.array([nx, ny])
                    coordinates_ft = np.array(coordinates_ft)
                    coordinates_fb = np.array(coordinates_fb)

                    # Calculate distances from centroid to fingertips and finger bases
                    d_centrid_ft = np.linalg.norm(coordinates_centroid - coordinates_ft, axis=1)
                    d_centrid_fb = np.linalg.norm(coordinates_centroid - coordinates_fb, axis=1)
                    dif = d_centrid_ft - d_centrid_fb
                    fingers = dif > 0
                    fingers = np.append(thumb_finger, fingers)
                    fingers_counter = str(np.count_nonzero(fingers==True))

                    # Adjust thickness of lines for drawing based on finger presence
                    for (i, finger) in enumerate(fingers):
                        if finger == True:
                            thickness[i] = -1

                    # Draw hand landmarks and connections on the frame
                    mp_drawing.draw_landmarks(
                        frame,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style())

            try:
                # Attempt to retrieve coordinates of fingertips and finger bases
                thumb_tip_coordinates = coordinates_thumb[0]
                index_finger_tip_coordinates = coordinates_fb[0]
                middle_finger_tip_coordinates = coordinates_fb[1]
                ring_finger_tip_coordinates = coordinates_fb[2]
                pinky_tip_coordinates = coordinates_fb[3]
            except IndexError:
                pass

            estado = ""
            # Extract coordinates of centroid and move mouse pointer accordingly
            coord = (((str(coordinates_centroid)[1:-1])).split(" "))
            print(coord)
            pyautogui.FAILSAFE = False
            if coord[0] and coord[1]:
                pyautogui.FAILSAFE = False
                pyautogui.moveTo((int(coord[0])*2), (int(coord[1])*2))
            else:
                print("Error: Las coordenadas no son válidas.")

            try:
                # Perform mouse click actions based on finger gestures detected
                if matches_lists(calculateRange(thumb_tip_coordinates)[0], calculateRange(index_finger_tip_coordinates)[0]):
                        if matches_lists(calculateRange(thumb_tip_coordinates)[1], calculateRange(index_finger_tip_coordinates)[1]):
                            pyautogui.click((int(coord[0])*2), (int(coord[1])*2), interval=1)
                elif matches_lists(calculateRange(thumb_tip_coordinates)[0], calculateRange(middle_finger_tip_coordinates)[0]):
                        if matches_lists(calculateRange(thumb_tip_coordinates)[1], calculateRange(middle_finger_tip_coordinates)[1]):
                            pyautogui.rightClick((int(coord[0])*2), (int(coord[1])*2), interval=1)
            except (NameError, IndexError, ValueError):
                pass

            # Perform additional mouse actions based on finger counts and thicknesses
            if fingers_counter == "1" and thickness[0] == 2 and thickness[1] == -1 and thickness[2] == 2:
                time.sleep(0.2)
                pyautogui.FAILSAFE = False
                pyautogui.click((int(coord[0])*2), (int(coord[1])*2), interval=1)
                estado = "click" 
            elif fingers_counter == "2" and thickness[0] == 2 and thickness[1] == -1 and thickness[2] == -1:
                time.sleep(0.2)
                pyautogui.FAILSAFE = False
                estado = "click derecho"
                pyautogui.click((int(coord[0])*2), (int(coord[1])*2), interval=1, button="right")

            # Draw UI elements (finger count and labels) on the frame
            cv2.rectangle(frame, (0, 0), (80, 80), (125, 220, 0), -1)
            cv2.putText(frame, fingers_counter, (15, 65), 1, 5, (255, 255, 255), 2)
            cv2.rectangle(frame, (100, 10), (150, 60), PEACH, thickness[0])
            cv2.putText(frame, "Pulgar", (100, 80), 1, 1, (255, 255, 255), 2)
            cv2.rectangle(frame, (160, 10), (210, 60), PURPLE, thickness[1])
            cv2.putText(frame, "Indice", (160, 80), 1, 1, (255, 255, 255), 2)
            cv2.rectangle(frame, (220, 10), (270, 60), YELLOW, thickness[2])
            cv2.putText(frame, "Medio", (220, 80), 1, 1, (255, 255, 255), 2)
            cv2.rectangle(frame, (280, 10), (330, 60), GREEN, thickness[3])
            cv2.putText(frame, "Anular", (280, 80), 1, 1, (255, 255, 255), 2)
            cv2.rectangle(frame, (340, 10), (390, 60), BLUE, thickness[4])
            cv2.putText(frame, "Menique", (340, 80), 1, 1, (255, 255, 255), 2)
            cv2.putText(frame, estado, (0, 120), 1, 1, (255, 255, 255), 2)

            # Display the processed frame with overlays
            cv2.imshow("Frame", frame)

            # Exit the loop and release resources on Esc key press
            if cv2.waitKey(1) & 0xFF == 27:
                break

    # Release video capture and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()
