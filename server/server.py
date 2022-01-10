from flask import Flask, request, jsonify, send_from_directory
import flask
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO, emit
from core import Core
import json
from eye_track import EyeTrack

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
# app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins='*')

coreProccess = Core()

cors = CORS(app, resources={r"/*": {"origins": "http://localhost:4200"}})


@app.route("/change_text_color/", methods=['GET'])
def change_text_color():
    rgba = json.loads(request.args['rgba'])
    return coreProccess.change_text_color(rgba)


@app.route("/change_background_color/", methods=['GET'])
def change_background_color():
    rgba = json.loads(request.args['rgba'])
    return coreProccess.change_background_color(rgba)


@app.route("/change_eye_comfort/", methods=['GET'])
def change_eye_comfort():
    rgba = json.loads(request.args['rgba'])
    return coreProccess.change_eye_comfort(rgba)


@app.route("/dark_mode/", methods=['GET'])
def dark_mode():
    active = json.loads(request.args['active'])
    return coreProccess.dark_mode(active)

@app.route("/set_highlight/", methods=['GET'])
def set_highlight():
    options =  json.loads(request.args['options'])
    return coreProccess.set_highlight(options)


@app.route("/set_file", methods=['POST'])
def set_file():
    socketio.emit('scroll', {'up': True})
    coreProccess.set_file()
    return coreProccess.send_pdf(False)


@app.route('/send-file/')
def send_js():
    return send_from_directory('./', 'pdf_to_proccess.pdf')


track = EyeTrack()


@app.route('/eye_tracking/')
def eye_tracking():
    active = json.loads(request.args['active'])
    print(active)
   
    if(active):
     
        track.capturing = True
        track.process_frame(socketio)
    else:
        track.capturing = False
        track.stop()
        # del track
    return jsonify({"success": "true"})


@app.route("/")
def work():

    return jsonify({"success": "true"})


if __name__ == "__main__":
    # app.run()
    socketio.run(app)
