import streamlit as st
from PIL import Image
import tempfile
import cv2
import imageio

# Function to extract frames and create GIF
def extract_frames(video_path, output_path, start_time, end_time, speed_multiplier):
    vidcap = cv2.VideoCapture(video_path)
    
    # Get the FPS of the video
    fps = vidcap.get(cv2.CAP_PROP_FPS)
    
    # Calculate the start and end frames
    start_frame = int(start_time * fps)
    end_frame = int(end_time * fps)
    
    vidcap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    success, frame = vidcap.read()
    current_frame = start_frame
    frames = []

    while success and current_frame <= end_frame:
        frames.append(frame)
        current_frame += 1
        success, frame = vidcap.read()
    
    if speed_multiplier != 1.0:
        frames = frames[::int(speed_multiplier)]

    # Save frames as GIF
    rgb_frames = [cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) for frame in frames]
    imageio.mimsave(output_path, rgb_frames, fps=fps/speed_multiplier)
    

# Streamlit app
st.title("Automatic GIF Creator from Videos")

uploaded_file = st.file_uploader("Choose a video file...", type=["mp4", "avi", "mov", "mkv"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False) as temp_video:
        temp_video.write(uploaded_file.read())
        temp_video_path = temp_video.name
    
    # Preview the uploaded video
    st.video(temp_video_path)

    start_time = st.number_input("Start Time (seconds)", min_value=0.0, value=0.0, step=0.1)
    end_time = st.number_input("End Time (seconds)", min_value=0.1, value=5.0, step=0.1)
    speed_multiplier = st.number_input("Speed Multiplier", min_value=0.1, max_value=10.0, value=1.0)

    if st.button("Create GIF"):
        output_gif_path = temp_video_path + ".gif"
        
        st.write("Creating GIF...")
        extract_frames(temp_video_path, output_gif_path, start_time, end_time, speed_multiplier)
        
        st.write("GIF created successfully!")

        gif = Image.open(output_gif_path)
        st.image(gif, caption="Generated GIF")

        # Read the GIF file as bytes
        with open(output_gif_path, "rb") as file:
            gif_bytes = file.read()

        # Provide a download button for the GIF
        st.download_button(
            label="Download GIF",
            data=gif_bytes,
            file_name="output.gif",
            mime="image/gif"
        )
