import cv2
import mediapipe as mp
import pygame
import time

# Initialize Pygame
pygame.init()

# Create a Pygame window with the same dimensions as your cv2 window
screen = pygame.display.set_mode((1280, 960))

# Initialize MediaPipe Hands.
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Initialize MediaPipe drawing.
mp_drawing = mp.solutions.drawing_utils

# set pointer x and y to a default position (0,0)
pointer_x = 0
pointer_y = 0

# Start capturing video from the webcam.
cap = cv2.VideoCapture(0)

time_in_column = 0
column = -1

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    # Flip the image horizontally for a later selfie-view display.
    # Convert the BGR image to RGB.
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

    # Process the image and detect hands.
    results = hands.process(image)



    # Draw the hand annotations on the image.
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            pointer_x, pointer_y = int(hand_landmarks.landmark[8].x * image.shape[1]), int(hand_landmarks.landmark[8].y * image.shape[0])

    # # Convert the image color back so it can be displayed correctly.
    # image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    image = pygame.image.frombuffer(image.tostring(), image.shape[1::-1], "RGB")

    # # Display the resulting image in the Pygame window
    # screen.blit(image, (0, 0))

    # Fill the screen with a color
    screen.fill((0, 0, 0))

    # Draw the pointer
    pygame.draw.circle(screen, (255, 0, 0), (pointer_x, pointer_y), 20)
    pygame.draw.circle(screen, (0, 255, 0), (pointer_x, pointer_y), (time_in_column * 20)/100)

    # split the screen into 10 columns
    column_width = 1280 // 10
    for i in range(1, 10):
        pygame.draw.line(screen, (100, 100, 100), (i * column_width, 0), (i * column_width, 960))

    # Label each column with a number from 0 to 9
    font = pygame.font.Font(None, 36)
    for i in range(12,22):
        text = font.render(str(i), True, (255, 255, 255))
        screen.blit(text, ((i-12) * column_width + 10, 10))

    # check if the pointer is in a column for a certain amount of time and print the number
    previous_column = column
    column = pointer_x // column_width

    if column != previous_column:
        time_in_column = 0
    else:
        time_in_column += 1
        if time_in_column == 100:
            print(previous_column + 12)
            time_in_column = 0

    pygame.display.flip()

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Release the webcam and close the window.
cap.release()
cv2.destroyAllWindows()
