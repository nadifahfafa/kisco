import streamlit as st
from PIL import Image
import numpy as np

def detect_smudge(image):
    # Convert the image to grayscale for processing
    gray_image = image.convert("L")
    gray_array = np.array(gray_image)

    # Define a threshold for smudge detection
    threshold = 200
    smudge_mask = gray_array > threshold

    # Calculate smudge percentage
    smudge_area = np.sum(smudge_mask)  # Count smudge pixels
    total_area = gray_array.size       # Total pixels in the image
    smudge_percentage = (smudge_area / total_area) * 100

    # Generate binary smudge mask image for display
    smudge_image = (smudge_mask * 255).astype(np.uint8)

    return Image.fromarray(smudge_image), smudge_percentage

st.title("Real-Time Smudge Detection with Smudge Coverage")

# Capture image from webcam
camera_image = st.camera_input("Capture an image to detect smudge")

if camera_image is not None:
    # Open the image and perform smudge detection
    img = Image.open(camera_image)
    smudge_img, smudge_percentage = detect_smudge(img)

    # Display the original and processed images
    st.image(img, caption="Original Image", use_column_width=True)
    st.image(smudge_img, caption="Detected Smudge", use_column_width=True)
    st.write(f"There are Smudge {int(smudge_percentage)}")


