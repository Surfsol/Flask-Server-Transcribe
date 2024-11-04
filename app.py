from flask import Flask, request, jsonify
import speech_recognition as sr #SpeechRecognition library assigned to sr

app = Flask(__name__) #??

@app.route("/transcribe", methods=["POST"]) # only accpets post requests
def transcribe_audio():
    print("1 Endpoint '/transcribe' was hit", request.files)
    if "audio" not in request.files:
        return jsonify({"error": "No audio file provided"}), 400
    print("2 Endpoint audio found")
    audio_file = request.files["audio"]
    print("3 Endpoint audio found")
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
