import subprocess
import os
import webview


def start_streamlit():
    # Start the Streamlit server as a subprocess
    streamlit_command = ["streamlit", "run", "budd.py", "--server.headless", "true"]
    env = os.environ.copy()
    subprocess.Popen(streamlit_command, env=env)


if __name__ == "__main__":
    # Start the Streamlit server
    start_streamlit()

    # Allow some time for the Streamlit server to start
    import time

    time.sleep(2)  # Adjust if necessary based on server startup time

    # Create a PyWebview window pointing to the Streamlit app
    webview.create_window("Streamlit App", "http://localhost:8501")
    webview.start()
