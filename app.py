import streamlit as st
import imageio
import cv2
import os

def create_gif(video_path, start_time, end_time, gif_path, speed_multiplier):
    # Open the video file
    video = cv2.VideoCapture(video_path)
    
    # Get the FPS of the original video
    fps = video.get(cv2.CAP_PROP_FPS)
    
    # Calculate the frame numbers for start and end times
    start_frame = int(start_time * fps)
    end_frame = int(end_time * fps)
    
    # Set the video to start at the start_frame
    video.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    
    frames = []
    success, frame = video.read()
    current_frame = start_frame
    
    while success and current_frame <= end_frame:
        frames.append(frame)
        current_frame += 1
        success, frame = video.read()
    
    video.release()
    
    # Adjust the speed of the GIF
    if speed_multiplier != 1.0:
        frames = frames[::int(speed_multiplier)]
    
    # Convert frames to RGB and save as GIF
    rgb_frames = [cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) for frame in frames]
    imageio.mimsave(gif_path, rgb_frames, fps=fps/speed_multiplier)

def main():
    st.title("Automatic GIF Creator from Videos")
    
    uploaded_file = st.file_uploader("Upload a Video", type=["mp4", "avi", "mov", "mkv"])
    
    if uploaded_file is not None:
        with open("temp_video.mp4", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.video("temp_video.mp4")
        
        start_time = st.number_input("Start Time (seconds)", min_value=0.0, value=0.0)
        end_time = st.number_input("End Time (seconds)", min_value=0.0, value=5.0)
        speed_multiplier = st.number_input("Speed Multiplier", min_value=0.1, max_value=10.0, value=1.0)
        
        if st.button("Create GIF"):
            if end_time > start_time:
                with st.spinner("Creating GIF..."):
                    gif_path = "output.gif"
                    create_gif("temp_video.mp4", start_time, end_time, gif_path, speed_multiplier)
                    st.success("GIF created successfully!")
                    st.image(gif_path)
                    
                    # Create a download button for the GIF
                    with open(gif_path, "rb") as file:
                        st.download_button(
                            label="Download GIF",
                            data=file,
                            file_name="output.gif",
                            mime="image/gif"
                        )
            else:
                st.error("End time must be greater than start time")

if __name__ == "__main__":
    main()
