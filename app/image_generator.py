import os
import urllib.parse
import requests

def generate_image(prompt: str, panel_num: int) -> str:
    try:
        # Format and encode the prompt for the URL
        formatted_prompt = f"comic book style artwork, panel illustration: {prompt}"
        encoded_prompt = urllib.parse.quote(formatted_prompt)
        
        # Pollinations image endpoint (100% free, no API key required)
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=512&height=512&nologo=true"
        
        # Download the image
        response = requests.get(image_url, timeout=30)
        
        if response.status_code == 200:
            os.makedirs("static/panels", exist_ok=True)
            file_path = f"static/panels/panel_{panel_num}.png"
            
            with open(file_path, "wb") as f:
                f.write(response.content)
                
            return file_path
        else:
            raise Exception(f"Failed to fetch image. Status code: {response.status_code}")

    except Exception as e:
        raise Exception(f"Pollinations AI Image Generation Error: {str(e)}")
