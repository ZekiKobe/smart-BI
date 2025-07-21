#!/usr/bin/env python
import requests
import json

def test_gemini_api():
    # Test with different models
    models = [
        "gemini-pro",
        "gemini-1.5-pro",
        "gemini-1.5-flash"
    ]
    
    api_key = "AIzaSyC75ct3TNPpdaVC3oo41QEUSfxFUW2OTFs"
    
    for model in models:
        print(f"\nTesting model: {model}")
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": "Hello, how are you?"
                        }
                    ]
                }
            ]
        }
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            print(f"Status Code: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                print(f"Success! Response: {result}")
                return True
            else:
                print(f"Error: {response.text}")
        except Exception as e:
            print(f"Exception: {e}")
    
    return False

if __name__ == "__main__":
    print("Testing Gemini API...")
    success = test_gemini_api()
    if success:
        print("\n✅ Gemini API is working!")
    else:
        print("\n❌ Gemini API is not working. Please check the API key.") 