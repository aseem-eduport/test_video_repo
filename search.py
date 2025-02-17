import streamlit as st

from server.brain.core_llms import llm
from server.utils.util import generate_response
from server.brain.transcription import generate_transcription_data

st.title("PHY Video Help Bot 📹")
st.text("I'm a helpful bot which helps you to find videos in the system.")
st.text("Currently I only support Neet Physics videos.")

question = st.chat_input("Say something")
audio_value = st.audio_input("Record a voice message")
# question = "gravitation field"
if question:
    generated_content, link = generate_response(question)
    st.write(generated_content)
    if link:
        st.link_button("Video", link)

if audio_value:
    audio_data = generate_transcription_data(audio_value)
    print(audio_data,"response data----->>>")
    if audio_data:
        generated_content, link = generate_response(audio_data)
        st.write(generated_content)
        if link:
            st.link_button("Video", link)