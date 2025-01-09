import openai
import speech_recognition as sr
import pyttsx3
import subprocess
import time
from flask import Flask, render_template, request, jsonify

# Set up the OpenAI API key
from config import OPENAI_API_KEY
openai.api_key = OPENAI_API_KEY

# Initialize the recognizer and TTS engine
recognizer = sr.Recognizer()

try:
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Speed of speech
    engine.setProperty('volume', 0.9)  # Volume level
except RuntimeError:
    print("eSpeak not installed. Installing now...")
    subprocess.run(["sudo", "apt-get", "install", "espeak", "-y"])
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 0.9)

# Flask web app setup
app = Flask(__name__, template_folder='templates')

# Function to convert text to speech
def speak_text(text):
    engine.say(text)
    engine.runAndWait()

# Function to get GPT-4 response
def get_gpt4_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error: {str(e)}"

# Flask routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.json.get('user_input')
    if not user_input:
        return jsonify({'error': 'No input provided'}), 400

    # Get response from GPT-4
    gpt4_response = get_gpt4_response(user_input)
    return jsonify({'response': gpt4_response})

if __name__ == "__main__":
    app.run(debug=True)

# Main function for live conversation
def live_conversation():
    print("Say 'stop' to end the conversation.")
    while True:
        try:
            # Capture audio from the microphone
            with sr.Microphone() as source:
                print("Listening...")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)

                # Convert speech to text
                user_input = recognizer.recognize_google(audio)
                user_input = user_input.lower()

                # Check if the user wants to stop the conversation
                if "stop" in user_input:
                    print("Conversation ended.")
                    speak_text("Conversation ended. Goodbye!")
                    break

                print(f"You: {user_input}")

                # Get response from GPT-4
                gpt4_response = get_gpt4_response(user_input)
                print(f"GPT-4: {gpt4_response}")

                # Speak out the GPT-4 response
                speak_text(gpt4_response)

        except sr.UnknownValueError:
            print("Sorry, I did not understand that. Could you please repeat?")
            speak_text("Sorry, I did not understand that. Could you please repeat?")
        except sr.RequestError as e:
            print(f"Could not request results, please check your internet connection. Error: {e}")
            speak_text("Could not request results, please check your internet connection.")
        except KeyboardInterrupt:
            print("Conversation interrupted.")
            break

# HTML template for the web interface
html_template = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GPT-4 Live Conversation</title>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
</head>
<body>
    <h1>GPT-4 Live Conversation</h1>
    <input type="text" id="user_input" placeholder="Enter your message here">
    <button onclick="sendMessage()">Send</button>
    <div id="response"></div>

    <script>
        function sendMessage() {
            const userInput = $('#user_input').val();
            $.ajax({
                url: '/get_response',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ user_input: userInput }),
                success: function(response) {
                    $('#response').text(response.response);
                },
                error: function() {
                    $('#response').text('Error getting response.');
                }
            });
        }
    </script>
</body>
</html>
"""

# Save the HTML template to index.html
with open('templates/index.html', 'w') as f:
    f.write(html_template)
