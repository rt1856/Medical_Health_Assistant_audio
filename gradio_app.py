import gradio as gr
import os
from dotenv import load_dotenv
load_dotenv()

from brain_of_the_doctor import encode_image, analyze_image_with_query
from voice_of_the_patient import record_audio, transcribe_with_groq
from voice_of_the_doctor import text_to_speech_with_elevenlabs

system_prompt = """You have to act as a professional doctor... (same as above)"""

AUDIO_PATH = "patient_audio.mp3"

def start_recording():
    record_audio(AUDIO_PATH)  # this should be non-blocking or thread-based if it's blocking
    return "Recording started..."

def stop_recording():
    return AUDIO_PATH, "Recording stopped. You can now submit."

def process_inputs(image_filepath):
    speech_to_text_output = transcribe_with_groq(GROQ_API_KEY=os.getenv("GROQ_API_KEY"), 
                                                 audio_filepath=AUDIO_PATH,
                                                 stt_model="whisper-large-v3")

    if image_filepath:
        doctor_response = analyze_image_with_query(
            query=system_prompt + speech_to_text_output,
            encoded_image=encode_image(image_filepath),
            model="meta-llama/llama-4-maverick-17b-128e-instruct"
        )
    else:
        doctor_response = "No image provided for me to analyze"

    audio_response_path = "final.mp3"
    text_to_speech_with_elevenlabs(input_text=doctor_response, output_filepath=audio_response_path)

    return speech_to_text_output, doctor_response, audio_response_path


with gr.Blocks() as demo:
    gr.Markdown("## VoiceBot AI Doctor")

    with gr.Row():
        start_btn = gr.Button("Start Recording")
        stop_btn = gr.Button("Stop Recording")
        record_status = gr.Textbox(label="Recording Status")

    stop_audio_path = gr.Textbox(visible=False)

    start_btn.click(fn=start_recording, outputs=record_status)
    stop_btn.click(fn=stop_recording, outputs=[stop_audio_path, record_status])

    image_input = gr.Image(type="filepath", label="Upload Image")

    submit_btn = gr.Button("Submit to AI Doctor")
    
    stt_output = gr.Textbox(label="Speech to Text")
    doctor_output = gr.Textbox(label="Doctor's Response")
    doctor_audio = gr.Audio(label="Doctor Speaks")

    submit_btn.click(fn=process_inputs, inputs=[image_input], outputs=[stt_output, doctor_output, doctor_audio])

demo.launch(debug=True)
