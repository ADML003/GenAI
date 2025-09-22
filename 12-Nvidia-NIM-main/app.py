import os
from openai import OpenAI
from dotenv import load_dotenv

# 🔒 Load environment variables from the root directory (parent folder)
# This will look for .env file in the GenAI root directory, not the current folder
load_dotenv(dotenv_path="../.env")

# 🛡️ Get API key from environment variable (NEVER hardcode keys!)
api_key = os.getenv("NVIDIA_API_KEY")

print("🔍 Debugging API Key Setup:")
print(f"API Key found: {'✅ Yes' if api_key else '❌ No'}")
if api_key:
    print(f"API Key preview: {api_key[:10]}...{api_key[-5:]}")
    print(f"API Key length: {len(api_key)} characters")
else:
    print("❌ NVIDIA_API_KEY not found in environment variables!")
    print("📝 Please check your .env file in the root GenAI directory")
    exit(1)

# 🚫 Check if still using placeholder
if api_key == "your_nvidia_api_key_here" or api_key == "nvapi-your_actual_api_key_goes_here":
    print("❌ You're still using the placeholder API key!")
    print("📝 Please replace the placeholder with your actual NVIDIA API key in the root .env file")
    print("🔗 Get your API key from: https://build.nvidia.com/")
    exit(1)

client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = api_key  # 🔐 Use environment variable instead of hardcoded key
)

print("\n🚀 Connecting to NVIDIA NIM...")

try:
    completion = client.chat.completions.create(
      model="nvidia/llama3-chatqa-1.5-70b",  # 🔄 Updated to working NVIDIA model
      messages=[{"role":"user","content":"what is machine learning?"}],
      temperature=0.5,
      top_p=1,
      max_tokens=1024,
      stream=True
    )

    print("🤖 AI Response:")
    print("-" * 50)
    
    for chunk in completion:
      if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")
    
    print("\n" + "-" * 50)
    print("✅ Response completed!")

except Exception as e:
    error_msg = str(e)
    print(f"❌ Error occurred: {error_msg}")
    
    if "401" in error_msg or "Unauthorized" in error_msg:
        print("\n� Authentication Error - API Key Issues:")
        print("1. ❌ Invalid API key format")
        print("2. ❌ API key has expired") 
        print("3. ❌ API key doesn't have access to NVIDIA NIM")
        print("4. ❌ Incorrect API key copied")
        print("\n💡 Solutions:")
        print("• Visit: https://build.nvidia.com/")
        print("• Generate a new API key")
        print("• Copy the FULL key (starts with 'nvapi-')")
        print("• Update your .env file")
    
    elif "404" in error_msg:
        print("\n🔍 Model Not Found:")
        print("• The model name might be incorrect")
        print("• Try these alternative models:")
        print("  - meta/llama3-70b-instruct")
        print("  - microsoft/phi-3-mini-4k-instruct")
        print("  - mistralai/mixtral-8x7b-instruct-v0.1")
    
    else:
        print(f"\n🔧 General troubleshooting:")
        print("1. Check your internet connection")
        print("2. Verify NVIDIA NIM service status")
        print("3. Try a different model")

