# 🌐 Import necessary libraries for HTTP requests, JSON handling, and UI creation
import requests  # 📡 For making HTTP requests to the Ollama API server
import json      # 📋 For parsing and creating JSON data structures
import gradio as gr  # 🎨 Gradio library for creating beautiful web-based UI interfaces

# 🏠 Local Ollama Server Configuration
# This URL points to the local Ollama server running on port 11434
# Ollama is a tool for running large language models locally
url = "http://localhost:11434/api/generate"  # 🔗 API endpoint for generating responses

# 📬 HTTP Headers Configuration
# These headers tell the server what type of data we're sending
headers = {
    'Content-Type': 'application/json'  # 📨 Specify that we're sending JSON data
}

# 📚 Global Chat History Storage
# This list stores all previous prompts to maintain conversation context
history = []  # 🗂️ Empty list to accumulate conversation history

def generate_response(prompt):
    """
    🤖 Main function to generate AI responses using the local Ollama model
    
    Args:
        prompt (str): User's input text/question
    
    Returns:
        str: AI-generated response from the codeguru model
    """
    
    # 📝 Add current user prompt to conversation history
    history.append(prompt)  # 🔄 Maintain context across multiple exchanges
    
    # 🔗 Combine all previous conversations into one continuous context
    final_prompt = "\n".join(history)  # 📖 Join all history with newlines for context
    
    # 📦 Prepare the request payload for Ollama API
    data = {
        "model": "codeguru",        # 🧠 Specify which model to use (custom CodeLlama model)
        "prompt": final_prompt,     # 💬 Send the complete conversation context
        "stream": False             # ⚡ Get complete response at once (not streaming)
    }
    
    # 🚀 Send POST request to Ollama server with the prompt
    response = requests.post(
        url,                        # 🎯 Target URL (localhost:11434)
        headers=headers,            # 📋 HTTP headers (Content-Type: application/json)
        data=json.dumps(data)       # 📊 Convert Python dict to JSON string
    )
    
    # ✅ Check if the request was successful (HTTP 200 OK)
    if response.status_code == 200:
        # 🎉 Success! Process the response
        response_text = response.text           # 📄 Get raw response text
        data = json.loads(response_text)        # 🔍 Parse JSON response to Python dict
        actual_response = data['response']      # 🎯 Extract the AI's actual response text
        return actual_response                  # 📤 Return the generated text to user
    else:
        # ❌ Error occurred - print error details for debugging
        print("error:", response.text)          # 🚨 Log error message to console
        return "Sorry, there was an error generating the response."  # 💔 User-friendly error message

# 🎨 Create Beautiful Gradio Web Interface
interface = gr.Interface(
    fn=generate_response,                                    # 🎯 Function to call when user submits
    inputs=gr.Textbox(                                      # 📝 Input component configuration
        lines=4,                                            # 📏 Multi-line textbox (4 rows)
        placeholder="Enter your Prompt"                     # 💡 Helper text for users
    ),
    outputs="text"                                          # 📤 Output will be simple text display
)

# 🚀 Launch the Web Interface
# This starts a local web server and opens the interface in your browser
interface.launch()  # 🌟 Make the chatbot accessible via web browser
