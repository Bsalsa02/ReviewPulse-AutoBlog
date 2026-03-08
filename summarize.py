import os
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai

# Setup AI
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

def main():
    # Read the first link from our file
    with open("links.txt", "r") as f:
        video_url = f.readline().strip()
    
    # Extract the ID (the part after v=)
    video_id = video_url.split("v=")[1]
    
    # 1. Get Transcript
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    text = " ".join([t['text'] for t in transcript])
    
    # 2. AI Magic
    prompt = f"Create a detailed gear review blog post from this transcript: {text}"
    response = model.generate_content(prompt)
    
    # 3. Save as a new Markdown file
    filename = f"review-{video_id}.md"
    with open(filename, "w") as f:
        f.write(response.text)

if __name__ == "__main__":
    main()
