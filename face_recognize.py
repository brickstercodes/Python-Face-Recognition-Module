import cv2
import numpy as np
import os

# Paths to the Haar cascade files for face and eye detection
face_haar_file = 'D:\\Python FaceRecogModule\\recog\\haarcascade_frontalface_default.xml'
eye_haar_file = 'D:\\Python FaceRecogModule\\recog\\haarcascade_eye.xml'

# Folder where face data is stored
datasets = 'D:\\Python FaceRecogModule\\recog\\datasets'

# Initialize OpenCV's face and eye detectors and webcam
face_cascade = cv2.CascadeClassifier(face_haar_file)
eye_cascade = cv2.CascadeClassifier(eye_haar_file)
webcam = cv2.VideoCapture(0)

# Initialize face counter
face_counter = 0

# Function to create a list of images and labels for training
def prepare_training_data(data_folder_path):
    # Initialize lists for images and labels
    images = []
    labels = []
    label_dict = {}

    # Get the directories (each directory contains images for one person)
    for dir_name in os.listdir(data_folder_path):
        label = len(label_dict)
        label_dict[dir_name] = label

        subject_dir_path = os.path.join(data_folder_path, dir_name)

        # Read images in the subject directory
        for image_name in os.listdir(subject_dir_path):
            image_path = os.path.join(subject_dir_path, image_name)
            image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

            # Append the image and label to the lists
            images.append(image)
            labels.append(label)

    return images, labels, label_dict

# Load training data
images, labels, label_dict = prepare_training_data(datasets)

# Convert images and labels lists into NumPy arrays
labels = np.array(labels, dtype=np.int32)

# Create the face recognition model
model = cv2.face.LBPHFaceRecognizer_create()
model.train(images, labels)

# Set your desired confidence threshold
confidence_threshold = 60

while True:
    # Capture frame from webcam
    ret, frame = webcam.read()

    if not ret:
        break

    # Apply brightness and contrast adjustment
    alpha = 1.5  # Contrast control (1.0-3.0)
    beta = 25    # Brightness control (0-100)
    adjusted_frame = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)

    # Convert the frame to grayscale for face detection
    gray = cv2.cvtColor(adjusted_frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale frame
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # Update face counter
    face_counter = len(faces)

    for (x, y, w, h) in faces:
        # Extract the region of interest (ROI) containing the face
        face_roi = gray[y:y + h, x:x + w]

        # Resize the face ROI for face recognition model
        face_roi_resized = cv2.resize(face_roi, (130, 100))

        # Try to recognize the face
        label_id, confidence = model.predict(face_roi_resized)

        # Determine the recognized name and confidence level
        recognized_name = "Unknown"
        if confidence < confidence_threshold:
            for name, id_ in label_dict.items():
                if id_ == label_id:
                    recognized_name = name
                    break

        # Draw rectangle around the face and display recognized name
        color = (0, 255, 0) if recognized_name != "Unknown" else (0, 0, 255)
        cv2.rectangle(adjusted_frame, (x, y), (x + w, y + h), color, 2)
        cv2.putText(adjusted_frame, f'{recognized_name} - Confidence: {confidence:.2f}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

        # Detect eyes within the face region
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = adjusted_frame[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyes:
            eye_roi = roi_gray[ey:ey+eh, ex:ex+ew]
            eye_resized = cv2.resize(eye_roi, (50, 25))  # Resize eye region for recognition
            # Perform eye recognition (you will need to implement this part)
            # Here you can check if the eye_resized matches any known patterns
            # If yes, you can perform some action or display some information

    # Display the frame with detected faces and face counter
    cv2.putText(adjusted_frame, f"Number of Faces: {face_counter}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.imshow('Face Recognition', adjusted_frame)

    # Check for the 'Esc' key press to exit
    key = cv2.waitKey(10)
    if key == 27:
        break

# Release the webcam and close all OpenCV windows
webcam.release()
cv2.destroyAllWindows()
