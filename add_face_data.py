import cv2
import sys
import os

# Path to the Haar cascade file for face detection
face_haar_file = 'D:\\Python FaceRecogModule\\recog\\haarcascade_frontalface_default.xml'
eye_haar_file = 'D:\\Python FaceRecogModule\\recog\\haarcascade_eye.xml'

# Folder where face data will be stored
datasets = 'D:\\Python FaceRecogModule\\recog\\datasets'

# Initialize OpenCV's face and eye detectors and webcam
face_cascade = cv2.CascadeClassifier(face_haar_file)
eye_cascade = cv2.CascadeClassifier(eye_haar_file)
webcam = cv2.VideoCapture(0)

# Function to create a directory for a new person
def create_person_directory(name):
    # Creates a directory for storing face data of a new person.
    path = os.path.join(datasets, name)
    if not os.path.isdir(path):
        os.mkdir(path)
    return path

# Check if the person's name is provided as a command-line argument
if len(sys.argv) < 2:
    print("Please provide the person's name as a command-line argument.")
    sys.exit(1)
name = sys.argv[1]

# Create a directory for the person
person_path = create_person_directory(name)

# Capture and store faces
count = 1
while count <= 100:
    # Read a frame from the webcam
    ret, im = webcam.read()
    if not ret:
        break

    # Adjust brightness and contrast
    alpha = 1.5  # Contrast control (1.0-3.0)
    beta = 25    # Brightness control (0-100)
    adjusted_image = cv2.convertScaleAbs(im, alpha=alpha, beta=beta)

    # Convert the adjusted image to grayscale for face detection
    gray = cv2.cvtColor(adjusted_image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale frame
    faces = face_cascade.detectMultiScale(gray, 1.3, 4)
    
    for (x, y, w, h) in faces:
        # Draw a rectangle around the detected face
        cv2.rectangle(adjusted_image, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = adjusted_image[y:y+h, x:x+w]

        # Detect eyes within the face region
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
        
        # Save the face image in the person's directory
        cv2.imwrite(os.path.join(person_path, f'{count}.png'), roi_color)
        count += 1
        
    # Display the image with detected faces
    cv2.imshow('OpenCV', adjusted_image)
    
    # Check for the 'Esc' key press to exit
    key = cv2.waitKey(10)
    if key == 27:
        break

# Release the webcam and close all OpenCV windows
webcam.release()
cv2.destroyAllWindows()
