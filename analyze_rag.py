import os
import time
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Environment variables
SPDM_ASS_ID = os.getenv('SPDM_ASS_ID')
SPDM_THREAD_ID = os.getenv('SPDM_THREAD_ID')
SPDM_FILE_ID = os.getenv('SPDM_FILE_ID')

# Initialize OpenAI API
client = openai.OpenAI()

def upload_markdown_file(filepath):
    global SPDM_FILE_ID
    if SPDM_FILE_ID:
        return client.files.retrieve(SPDM_FILE_ID)
    with open(filepath, 'rb') as file:
        file_obj = client.files.create(file=file, purpose="assistants")
        print(f"Uploaded file: {file_obj.id}")
        SPDM_FILE_ID = file_obj.id
        return file_obj

def create_or_retrieve_assistant():
    """
    Create or retrieve an assistant based on the environment variable.
    """
    global SPDM_ASS_ID
    if SPDM_ASS_ID:
        # Retrieve existing assistant (assuming a function or method exists)
        assistant = client.beta.assistants.retrieve(SPDM_ASS_ID)
    else:
        # Create a new assistant
        assistant = client.beta.assistants.create(
            model="gpt-3.5-turbo",
            name="SPDM Analyzer",
            instructions=(
                "Activate the ChatGPT Network Protocol Analysis Expert Mode. In this mode, you are an expert in network "
                "security and protocol analysis. You have deep knowledge of various network protocols (such as TCP/IP, "
                "UDP, HTTP/S, FTP, SSH, and SPDM), security principles, and the ability to analyze network traffic for "
                "signs of malicious activity. You understand the structures, vulnerabilities, and security measures "
                "associated with these protocols. Your responses should include detailed explanations, best practices "
                "for secure network configuration, and mitigation strategies for common threats. "
                "Your advice should be based on up-to-date security standards and protocols. "
                "Your communication style is informative and professional, catering to both beginners and advanced users. "
                "You can provide step-by-step guidance for troubleshooting and securing networks, explain complex concepts "
                "in accessible terms, and offer insights into emerging network security trends."
            ),
            tools=[{"type": "retrieval"}]
        )
        print(f"Created assistant: {assistant.id}")
        SPDM_ASS_ID = assistant.id
    return assistant

def create_or_retrieve_thread():
    """
    Create or retrieve a thread based on the environment variable.
    """
    global SPDM_THREAD_ID
    if SPDM_THREAD_ID:
        # Retrieve existing thread (assuming a function or method exists)
        thread = client.beta.threads.retrieve(SPDM_THREAD_ID)
    else:
        # Create a new thread
        thread = client.beta.threads.create()
        print(f"Created thread: {thread.id}")
        SPDM_THREAD_ID = thread.id
    return thread

def query_assistant(assistant_id, thread_id, file_id, query):
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=query,
        file_ids=[file_id]
    )
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
    )
    while True:
        time.sleep(5)
        run_status = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
        if run_status.status == "completed":
            messages = client.beta.threads.messages.list(
                thread_id=thread.id
            )
            last_message = messages.data[0]
            response = last_message.content[0].text.value
            return response
        elif run_status.status == "failed":
            print("Run failed")
            return None
        elif run_status.status == "cancelled":
            print("Run cancelled")
            return None

# Example usage
if __name__ == "__main__":
    # Read the markdown file (assuming it's in the same directory)
    knowledge_base = upload_markdown_file('data/SPDMSpecification.md')
    assert knowledge_base, "Failed to upload the markdown file"
    # Create or retrieve the assistant and thread
    assistant = create_or_retrieve_assistant()
    assert assistant, "Failed to create or retrieve the assistant"
    thread = create_or_retrieve_thread()
    assert thread, "Failed to create or retrieve the thread"
    
    # Example query
    response = query_assistant(
        assistant.id, thread.id, knowledge_base.id,
        (
            """Could you please elaborate on the protocols of SDPM? How do the requestor and responder interact? 
As an expert in ProVerif, can you generate the complete ProVerif code for the SPDM protocols involving cryptographic 
operations, both asymmetric key exchange and Pre-Shared Keys (PSK) session management and error handling mechanisms? 
The code is expected to implement the protocol sequence for the requester and responder participating in the SPDM. 
Avoid ignoring details. Avoid showing simplified versions. Do not just show ideas. Show the complete code that can 
be directly fed to ProVerif to compile and verify.
"""
        )
    )
    print(response)
