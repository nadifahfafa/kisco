import streamlit as st
import qrcode
from PIL import Image
import io
import speech_recognition as sr  # Will only work in a local environment with microphone access

# Menu with items and prices
menu = {
    "burger": 5.99,
    "pizza": 8.99,
    "coffee": 2.99,
    "salad": 4.99,
    "soda": 1.99
}

# Initialize an empty list to store orders
if 'order_list' not in st.session_state:
    st.session_state['order_list'] = []
if 'total_price' not in st.session_state:
    st.session_state['total_price'] = 0.0

# Function to generate QR code
def generate_qr_code(url):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    
    # Convert the image to a format suitable for Streamlit
    img_byte_array = io.BytesIO()
    img.save(img_byte_array, format='PNG')
    img_byte_array = img_byte_array.getvalue()
    
    return img_byte_array

# Voice recognition function (only works locally)
def recognize_speech():
    recognizer = sr.Recognizer()
    
    try:
        mic = sr.Microphone()
        st.write("Listening for your order...")

        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            order = recognizer.recognize_google(audio).lower()  # Convert to lowercase for easier matching
            st.write(f"You said: {order}")
            return order
        except sr.UnknownValueError:
            st.error("Sorry, I didn't catch that. Please try again.")
            return None
        except sr.RequestError:
            st.error("API unavailable")
            return None
    except Exception as e:
        st.error("Microphone not available. Please check your device.")
        return None

# Function to process the order, update total, and display price
def process_order(order):
    if order in menu:
        price = menu[order]
        st.session_state['order_list'].append((order, price))
        st.session_state['total_price'] += price
        st.success(f"Added {order.capitalize()} - ${price:.2f} to your order.")
    else:
        st.error(f"Item '{order}' not found in the menu. Please try again.")

# App interface
st.title("Touchless Kiosk Ordering System")

# Generate a QR code for mobile interaction
url = "https://your-ordering-system.com"  # Replace with actual ordering site URL
st.write("Scan the QR code to use the ordering system on your phone:")

# Display the QR code
qr_image = generate_qr_code(url)
st.image(qr_image, caption="Scan to place your order", use_column_width=True)

st.write("Or use voice commands to place your order (works locally):")

# Button to start voice recognition (only works locally)
if st.button("Start Voice Command"):
    order = recognize_speech()
    if order:
        process_order(order)

# Display the order summary and total
if st.session_state['order_list']:
    st.write("### Your Order:")
    for item, price in st.session_state['order_list']:
        st.write(f"- {item.capitalize()} - ${price:.2f}")
    
    st.write(f"### Total Price: ${st.session_state['total_price']:.2f}")

st.write("No need to touch the screen. Stay safe!")
