from flask import Flask, request, jsonify
import speech_recognition as sr #SpeechRecognition library assigned to sr

app = Flask(__name__) #??

@app.route("/transcribe", methods=["POST"]) #only accpets post requests
def transcribe_audio():
    if "audio" not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files["audio"]
    recognizer = sr.Recognizer() # Opens audio file as an audio source, to recognize and record.
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source) # audio file into audio_data, making it ready for transcription
        print(audio_data)
        try:
            text = recognizer.recognize_google(audio_data)
            return jsonify({"text": text})
        except sr.UnknownValueError:
            return jsonify({"error": "Could not understand audio"}), 400
        except sr.RequestError as e:
            return jsonify({"error": f"Could not request results; {e}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
