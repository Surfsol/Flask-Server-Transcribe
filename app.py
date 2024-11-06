from flask import Flask, request, jsonify
import speech_recognition as sr #SpeechRecognition library assigned to sr
import base64
from io import BytesIO

app = Flask(__name__) #??

@app.route("/transcribe", methods=["POST"]) # only accpets post requests
def transcribe_audio():
    print("1 Endpoint '/transcribe' was hit", request.files)
    data = request.get_json()
    print(data.keys())
    if "audio" in request.files:
        print("2 Endpoint audio found in request.files")
        audio_file = request.files["audio"]
    elif request.is_json and "audio" in request.get_json():
        print("2 Endpoint audio found in request.get_json")
        audio_data = base64.b64decode(data["audio"])
        audio_file = BytesIO(audio_data)
    else:
        return jsonify({"error": "No audio file provided"}), 400

    recognizer = sr.Recognizer() # Opens audio file as an audio source, to recognize and record.
    with sr.AudioFile(audio_file) as source:
        print("4 inside")
        audio_data = recognizer.record(source) # audio file into audio_data, making it ready for transcription
        print('5', audio_data)
        try:
            print('6', audio_data)
            text = recognizer.recognize_sphinx(audio_data)
            print("7 Sphinx thinks you said " + text)
            return jsonify({"text": text})
        except sr.UnknownValueError:
            print("Sphinx could not understand audio")
            return jsonify({"error": "Could not understand audio"}), 400
        except sr.RequestError as e:
            print("Sphinx error; {0}".format(e))
            return jsonify({"error": f"Could not request results; {e}"}), 500   

if __name__ == "__main__":
    app.run(debug=True)
