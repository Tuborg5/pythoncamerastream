from flask import Flask, Response
import cv2

# Initialize the Flask app
app = Flask(__name__)

# Initialize the camera
camera = cv2.VideoCapture(0)  # 0 is usually the default camera index for Pi Camera Module

# Set camera resolution (adjust according to your Camera Module 3 capabilities)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


def generate_frames():
    """Generates video frames for streaming."""
    while True:
        success, frame = camera.read()  # Read a frame from the camera
        if not success:
            break
        else:
            # Encode the frame in JPEG format
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Yield the frame in byte format
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Route to stream video to the web interface."""
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    """Main page displaying the video stream."""
    return '''
    <html>
        <head>
            <title>Raspberry Pi Camera Stream</title>
        </head>
        <body>
            <h1>Raspberry Pi Camera Stream</h1>
            <img src="/video_feed" width="640" height="480">
        </body>
    </html>
    '''

if __name__ == '__main__':
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)
