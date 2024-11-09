================================
 # speech-bot-assignment
 ===============================

 Functionalities
 ---------------

1.Speech-to-Text (get_speech_input):

Captures audio from the microphone and transcribes it into text using Google’s Speech Recognition API via the SpeechRecognition library.
The function retries up to 3 times if it fails to recognize speech and prompts the user to repeat.

2.Question Answering (get_answer):

Sends the transcribed question to OpenAI's gpt-3.5-turbo model to generate an answer.
This function handles the core knowledge processing and generation task, providing an answer based on the user’s input.

3.Text-to-Speech (speak_text):

Converts the generated answer text into spoken form using the pyttsx3 library, which operates offline and supports voice playback.

4.Sentiment Analysis (analyze_sentiment):

After the user provides feedback on the answer, this function analyzes the sentiment of the feedback.
Using the OpenAI API, it categorizes the feedback as "positive," "neutral," or "negative" to gauge the user’s satisfaction.

5.Feedback Loop:

After providing an answer, the program prompts the user to provide feedback (e.g., "yes," "no," or "it was helpful").
Based on the feedback, the assistant detects sentiment and speaks back the sentiment result to close the loop with the user.


Metrics
---------------------------

1.Latency:
The latency_list tracks the time taken for each answer generation using the OpenAI API.
We calculate the average latency after each session in display_metrics.


2.Memory Usage:
memory_usage_list logs memory usage during each interaction, helping track resource consumption.
Average memory usage is displayed in display_metrics.

3.Throughput:
throughput_count increments for each question successfully processed, showing the total number of processed requests.


4.Response Accuracy:
response_accuracies logs successful answers as 1 and failures as 0. Average accuracy gives an idea of how often the assistant answered correctly.


5.Sentiment Analysis Accuracy:
sentiment_accuracies logs the success or failure of sentiment analysis based on expected sentiments like "positive" or "negative."


Pre-requisites
--------------------

--install below dependencies

pip install openai SpeechRecognition pyttsx3 pyaudio psutil

 --set API key

 On Windows (PowerShell)
$env:OPENAI_API_KEY="your_openai_api_key"
