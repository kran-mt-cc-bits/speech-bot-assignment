import os
import speech_recognition as sr
import pyttsx3
import openai
import time
import psutil  # For memory usage monitoring

# Load OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize the text-to-speech engine
tts_engine = pyttsx3.init()
tts_engine.setProperty('rate', 150)  # Set speaking rate
tts_engine.setProperty('volume', 0.9)  # Set volume

# LLMOps Metrics Tracking
latency_list = []
memory_usage_list = []
throughput_count = 0
response_accuracies = []  # Placeholder for response accuracy evaluation
sentiment_accuracies = []  # Placeholder for sentiment accuracy based on user feedback

def get_speech_input(prompt, retries=3):
    """
    Captures spoken input from the microphone and converts it to text.
    Retries if it fails to recognize speech.
    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print(prompt)
        speak_text(prompt)  # Prompt the user via speech
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source)

    attempt = 0
    while attempt < retries:
        try:
            # Measure memory usage
            memory_usage = psutil.Process().memory_info().rss / (1024 * 1024)  # MB
            memory_usage_list.append(memory_usage)
            
            # Use Google's speech recognition to transcribe the audio
            text = recognizer.recognize_google(audio)
            print(f"Text heard: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I did not understand the speech. Please try again.")
            attempt += 1
            if attempt < retries:
                speak_text("Sorry, I didn't catch that. Could you please repeat?")
                with sr.Microphone() as source:
                    audio = recognizer.listen(source)  # Retry listening
        except sr.RequestError:
            print("Could not request results from the speech recognition service.")
            return None

    print("Failed to capture speech after multiple attempts.")
    return None

def get_answer(question):
    """
    Uses OpenAI's GPT model to generate an answer to the given question.
    Measures latency and records memory usage.
    """
    global throughput_count
    start_time = time.time()

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": question}],
            max_tokens=50,
            temperature=0.5
        )
        latency = time.time() - start_time
        latency_list.append(latency)

        # Record memory usage
        memory_usage = psutil.Process().memory_info().rss / (1024 * 1024)
        memory_usage_list.append(memory_usage)

        answer_text = response['choices'][0]['message']['content'].strip()
        print(f"Answer generated: {answer_text}")
        
        # Increment throughput count
        throughput_count += 1
        response_accuracies.append(1)  # Placeholder for manual evaluation later
        return answer_text
    except Exception as e:
        print(f"Error getting answer: {e}")
        response_accuracies.append(0)  # Indicate failure in response accuracy
        return "I'm sorry, I couldn't get the answer at the moment."

def analyze_sentiment(feedback):
    """
    Uses OpenAI's Chat Completion API with gpt-3.5-turbo to detect sentiment of feedback.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that analyzes the sentiment of feedback. Please respond with 'positive', 'neutral', or 'negative'."},
                {"role": "user", "content": f"Sentiment of the feedback: '{feedback}'"}
            ],
            max_tokens=10,
            temperature=0
        )
        sentiment_text = response['choices'][0]['message']['content'].strip().lower()
        print(f"Sentiment detected: {sentiment_text}")
        
        # Placeholder for manual evaluation: assume sentiment detection success
        sentiment_accuracies.append(1 if "positive" in sentiment_text or "negative" in sentiment_text else 0)
        return sentiment_text
    except Exception as e:
        print(f"Error analyzing sentiment: {e}")
        sentiment_accuracies.append(0)  # Indicate failure in sentiment accuracy
        return "Unable to analyze sentiment."

def speak_text(text):
    """
    Converts text to speech and plays it back.
    """
    print(f"Speaking: {text}")
    tts_engine.say(text)
    tts_engine.runAndWait()

def display_metrics():
    """
    Displays the collected metrics for analysis.
    """
    print("\n--- LLMOps Metrics ---")
    print(f"Total Requests Processed (Throughput): {throughput_count}")
    print(f"Average Latency (seconds): {sum(latency_list) / len(latency_list) if latency_list else 0}")
    print(f"Average Memory Usage (MB): {sum(memory_usage_list) / len(memory_usage_list) if memory_usage_list else 0}")
    print(f"Response Accuracy: {sum(response_accuracies) / len(response_accuracies) * 100 if response_accuracies else 0}%")
    print(f"Sentiment Analysis Accuracy: {sum(sentiment_accuracies) / len(sentiment_accuracies) * 100 if sentiment_accuracies else 0}%")

def main():
    """
    Main loop that listens for a question, gets an answer, asks for feedback, and analyzes feedback sentiment.
    """
    while True:
        print("\n--- Ask a General Knowledge Question ---")
        
        # Get a question via speech input
        question = get_speech_input("Please ask your question. Say 'exit' to end the session.")
        
        # Check if the user said "exit"
        if question and question.lower() == "exit":
            print("Exiting the session and displaying metrics.")
            break
        
        if question is None:
            continue
        
        # Generate an answer
        answer = get_answer(question)
        
        # Speak the answer
        speak_text(answer)

        # Ask for feedback
        feedback_prompt = "Did that answer your question? Please say 'yes', 'no', or 'it was helpful.'"
        feedback = get_speech_input(feedback_prompt)
        if feedback:
            # Perform sentiment analysis on the feedback
            sentiment = analyze_sentiment(feedback)
            
            # Speak the sentiment result
            speak_text(f"Your feedback sentiment is detected as: {sentiment}")
        
        # Pause before the next question
        time.sleep(2)
    
    # Display metrics after session
    display_metrics()

if __name__ == "__main__":
    main()
