import streamlit as st
from dotenv import load_dotenv
load_dotenv() #Load all the enviorment variable
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt="""you are Youtube video summarizer. You will taking text
and summarizeing the entire video and providing the important summery in points
within 300 words. The transcript text is here, provide summery :"""

## getting the transcript data from yt videos
def extract_transcript_details(youtube_video_url):
    try:
        video_id=youtube_video_url.split("=")[1]
        transcript_text=YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]
    
        return transcript

    except Exception as e:
        raise e

## getting the summery based on Prompt from Google Gemimi Pro
def generate_gemini_content(transcript_text, prompt):

    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content(prompt+transcript_text)
    return response.text

st.title("youtube Transcript to Summery Converter")
youtube_link = st.text_input("Enter Youtube link:")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Get Detail Notes"):
    transcript_text=extract_transcript_details(youtube_link)

    if transcript_text:
        summery=generate_gemini_content(transcript_text, prompt)
        st.markdown("## Detail Summery :")
        st.write(summery)