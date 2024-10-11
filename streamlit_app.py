import streamlit as st
import numpy as np
from PIL import Image, ImageOps, ImageFilter

# Function to detect dirt/smudges on a screen
def detect_dirt(image, low_threshold, high_threshold):
    # Convert image to grayscale
    gray_image = ImageOps.grayscale(image)
    
    # Apply Gaussian blur to reduce noise
    blurred_image = gray_image.filter(ImageFilter.GaussianBlur(5))
    
    # Convert the blurred image to a NumPy array for processing
    image_array = np.array(blurred_image)
    
    # Simple edge detection using NumPy
    edges = np.zeros_like(image_array)
    edges[1:-1, 1:-1] = np.abs(image_array[2:, 1:-1] - image_array[:-2, 1:-1]) + \
                        np.abs(image_array[1:-1, 2:] - image_array[1:-1, :-2])
    
    # Create a binary mask based on thresholding to detect smudges
    dirt_mask = (edges > low_threshold) & (edges < high_threshold)
    
    # Convert the mask back to an image for display
    dirt_highlight = Image.fromarray(np.uint8(dirt_mask) * 255)
    
    return dirt_mask, dirt_highlight

# Streamlit app interface
st.title("Continuous Dirt & Smudge Detection (Camera Input)")

st.write("This application continuously detects dirt or smudges using your camera input.")

# Sidebar for adjustable detection parameters
st.sidebar.header("Detection Sensitivity")
low_threshold = st.sidebar.slider('Low Threshold', 0, 100, 30)
high_threshold = st.sidebar.slider('High Threshold', 100, 255, 150)

# Camera input for real-time image capture
st.write("Place your screen in front of the camera and stay still for a moment to analyze for dirt.")
camera_image = st.camera_input("Start capturing frames")

if camera_image is not None:
    # Load the captured frame with Pillow
    image = Image.open(camera_image)
    
    # Display the captured frame
    st.image(image, caption="Captured Frame", use_column_width=True)
    
    st.write("Analyzing the frame for dirt or smudges...")

    # Call the dirt detection function
    dirt_mask, dirt_highlight = detect_dirt(image, low_threshold, high_threshold)

    # Feedback on the analysis result
    num_smudges = np.sum(dirt_mask)
    
    if num_smudges > 0:
        st.warning(f"Detected {num_smudges} potential smudges or dirt spots.")
    else:
        st.success("The screen appears clean!")
    
    # Display the processed image highlighting dirt/smudges
    st.image(dirt_highlight, caption="Highlighted Dirt/Smudges", use_column_width=True)
else:
    st.write("Waiting for camera input... Please ensure your camera is enabled.")
