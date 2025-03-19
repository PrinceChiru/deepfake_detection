import streamlit as st
import os
import subprocess

# Ensure temp directory exists
temp_dir = "temp"
os.makedirs(temp_dir, exist_ok=True)

def process_file(uploaded_file):
    """Save the uploaded file and run the appropriate model for prediction."""
    file_path = os.path.join(temp_dir, uploaded_file.name)
    
    # Save the uploaded file
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.write(f"✅ File uploaded: {uploaded_file.name}")

    # Choose the correct prediction script
    if uploaded_file.type.startswith("image"):
        command = ["python", "backend/img_pred.py", file_path]
    elif uploaded_file.type.startswith("video"):
        command = ["python", "backend/vid_pred.py", file_path]
    else:
        st.error("❌ Unsupported file type. Please upload an image or video.")
        return

    # Run the script
    st.write(f"🚀 Running prediction on {uploaded_file.name} ...")
    result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace")


    if result.returncode != 0:
        st.error(f"❌ Error: {result.stderr}")
    else:
        st.success("✅ Prediction Completed!")
        st.write("### Prediction Result:")
        if result.stdout:
            st.write(result.stdout)
        else:
            st.error("⚠️ No valid output received. Please check the input file and try again.")


    # Clean up temp file
    os.remove(file_path)
    st.write("🗑️ Temporary file deleted.")

# Streamlit UI
st.title("Deepfake Detection System")
st.write("Upload an **image or video** to check if it's **real or fake**.")

uploaded_file = st.file_uploader("Choose an image or video...", type=["jpg", "png", "mp4", "avi", "mov", "mkv"])

if uploaded_file is not None:
    process_file(uploaded_file)