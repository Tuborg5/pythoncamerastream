from flask import Flask, render_template, Response
import picamera2
import time
import os
import cv2  # OpenCV for encoding frames

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def generate_stream():
    with picamera2.Picamera2() as camera:
        try:
            config = camera.create_preview_configuration(main={"size": (1536, 864), "format": "RGB888"})  # Use RGB format
            camera.configure(config)

            camera.start()

            while True:
                # Capture a frame as an array
                frame_array = camera.capture_array('main')

                # Encode the frame to JPEG
                _, frame_jpeg = cv2.imencode('.jpg', frame_array)
                frame_bytes = frame_jpeg.tobytes()

                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
                time.sleep(1/30)  # Frame rate control
                # No need to remove files since we're using arrays

        except Exception as e:
            print("Error in generate_stream:", e)

@app.route('/video')
def video_feed():
    return Response(generate_stream(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)  # Make it accessible from external networks
