import requests
import time
import os

# Set your OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")  # Or replace with your actual API key if not using environment variables

# Step 1: Upload the training file
file_path = 'data_converted.jsonl'  # Path to your training data file

with open(file_path, 'rb') as f:
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    files = {
        'file': f
    }
    data = {
        "purpose": "fine-tune"
    }

    response = requests.post("https://api.openai.com/v1/files", headers=headers, files=files, data=data)

    if response.status_code == 200:
        file_response = response.json()
        file_id = file_response["id"]
        print(f"File uploaded successfully with ID: {file_id}")
    else:
        print(f"Error uploading file: {response.text}")
        exit()

# Step 2: Create a fine-tuning job
url = "https://api.openai.com/v1/fine_tuning/jobs"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}
data = {
    "training_file": file_id,
    "model": "gpt-3.5-turbo"  # Ensure this model is supported by your OpenAI account
}

response = requests.post(url, headers=headers, json=data)

if response.status_code == 200:
    fine_tune_response = response.json()
    fine_tune_job_id = fine_tune_response["id"]
    print(f"Fine-tuning job created with ID: {fine_tune_job_id}")
else:
    print(f"Error creating fine-tuning job: {response.text}")
    exit()

# Step 3: Monitor the fine-tuning job status
while True:
    response = requests.get(f"https://api.openai.com/v1/fine_tuning/jobs/{fine_tune_job_id}", headers=headers)
    if response.status_code == 200:
        status_response = response.json()
        status = status_response["status"]
        print(f"Fine-tuning job status: {status}")

        if status in ["succeeded", "failed"]:
            break
    else:
        print(f"Error checking job status: {response.text}")
        break

    time.sleep(60)  # Wait for a minute before checking again

# Step 4: Use the fine-tuned model if successful
if status == "succeeded":
    message_data = {
        "model": status_response["fine_tuned_model"],
        "messages": [
            {"role": "user", "content": "What is the capital of France?"}
        ]
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=message_data)
    
    if response.status_code == 200:
        answer = response.json()["choices"][0]["message"]["content"]
        print(f"Response from fine-tuned model: {answer}")
    else:
        print(f"Error using the fine-tuned model: {response.text}")
else:
    print("Fine-tuning job did not succeed.")
