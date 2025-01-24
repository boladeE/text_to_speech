import boto3
import speech_recognition as sr
import os

# Initialize Amazon Polly for TTS
polly_client = boto3.client(
    "polly",
    aws_access_key_id="YOUR_AWS_ACCESS_KEY",
    aws_secret_access_key="YOUR_AWS_SECRET_KEY",
    region_name="us-east-1"  # Change this to your preferred AWS region
)

# Speech-to-Text function using Google Speech Recognition
def speech_to_text():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    print("Adjusting for ambient noise... Please wait.")
    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        print("Recognizing speech...")
        text = recognizer.recognize_google(audio)
        print(f"User said: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand the audio.")
        return None
    except sr.RequestError as e:
        print(f"Error with the Speech Recognition service: {e}")
        return None

# Text-to-Speech function using Amazon Polly
def text_to_speech(text):
    try:
        print("Converting text to speech...")
        response = polly_client.synthesize_speech(
            Text=text,
            OutputFormat="mp3",
            VoiceId="Joanna"  # You can change this to other available voices
        )

        # Save the audio file
        audio_file = "response.mp3"
        with open(audio_file, "wb") as file:
            file.write(response["AudioStream"].read())
        
        # Play the audio file
        os.system(f"start {audio_file}" if os.name == "nt" else f"afplay {audio_file}")

    except Exception as e:
        print(f"Error with Amazon Polly: {e}")

# Main program
if __name__ == "__main__":
    while True:
        print("\n--- Voice Interaction System ---")
        user_input = speech_to_text()

        if user_input:
            # Generate a response (simple echo for this example)
            response = f"You said: {user_input}. How can I assist further?"
            print(f"Response: {response}")

            # Convert the response to speech
            text_to_speech(response)
        else:
            print("Please try again.")
