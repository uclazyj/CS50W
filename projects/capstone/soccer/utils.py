from PIL import Image
from google import genai
import json
import time

def extract_names_from_image(image_path):
    client = genai.Client()
    img = Image.open(image_path)
    prompt = """
    Extract all human names from this image. 
    Return the names as a JSON object with a single key 'names' containing a list of strings.
    Example: {"names": ["John Doe", "Jane Smith"]}
    """
    num_api_tries = 3
    for _ in range(num_api_tries):
        try:
            # Use Gemini 3 Flash (fast & cost-effective) or Gemini 3 Pro (for complex layouts)
            response = client.models.generate_content(
                model="gemini-3-flash-preview",
                contents=[prompt,img],
                config={
                    "response_mime_type": "application/json"
                }
            )

            print("API call returns successfully")

            data = json.loads(response.text)
            names_list = data.get("names", [])
            return names_list
        
        except Exception as e:
            print(f"Error extracting names from image using GEMINI API: {e}")
            time.sleep(1)
    
    return []