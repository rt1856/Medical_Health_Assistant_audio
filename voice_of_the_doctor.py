
# Step 1a: Setup Text to Speech – TTS – model with gTTS
import os
from gtts import gTTS
import subprocess
import platform
from pydub import AudioSegment
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

# Function to play audio cross-platform
def play_audio(filepath_mp3):
    os_name = platform.system()

    if os_name == "Windows":
        # Convert to WAV for Windows SoundPlayer
        filepath_wav = filepath_mp3.replace(".mp3", ".wav")
        sound = AudioSegment.from_mp3(filepath_mp3)
        sound.export(filepath_wav, format="wav")
        try:
            subprocess.run([
                'powershell', '-c',
                f'(New-Object Media.SoundPlayer "{filepath_wav}").PlaySync();'
            ])
        except Exception as e:
            print(f"Windows playback error: {e}")
    elif os_name == "Darwin":  # macOS
        subprocess.run(['afplay', filepath_mp3])
    elif os_name == "Linux":
        subprocess.run(['mpg123', filepath_mp3])  # Requires mpg123 installed
    else:
        raise OSError("Unsupported operating system")

# gTTS basic save only
def text_to_speech_with_gtts_old(input_text, output_filepath):
    language = "en"
    audioobj = gTTS(text=input_text, lang=language, slow=False)
    audioobj.save(output_filepath)

input_text="hii this is Riddhi"
# gTTS with autoplay
def text_to_speech_with_gtts(input_text, output_filepath):
    language = "en"
    audioobj = gTTS(text=input_text, lang=language, slow=False)
    audioobj.save(output_filepath)
    play_audio(output_filepath)

input_text="Hi this is autoplay testings"
# ElevenLabs basic save only
from elevenlabs.client import ElevenLabs
import elevenlabs

def text_to_speech_with_elevenlabs_old(input_text, output_filepath):
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio = client.generate(
        text=input_text,
        voice="Aria",
        output_format="mp3_22050_32",
        model="eleven_turbo_v2"
    )
    elevenlabs.save(audio, output_filepath)

# ElevenLabs with autoplay
def text_to_speech_with_elevenlabs(input_text, output_filepath):
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio = client.generate(
        text=input_text,
        voice="Aria",
        output_format="mp3_22050_32",
        model="eleven_turbo_v2"
    )
    elevenlabs.save(audio, output_filepath)
    play_audio(output_filepath)

# Sample usage
#input_text = "Hi this is AI with Riddhi, autoplay testing with gTTS!"
#text_to_speech_with_gtts(input_text=input_text, output_filepath="gtts_testing_autoplay.mp3")

#input_text = "Hi this is AI with Riddhi, autoplay testing with ElevenLabs!"
#text_to_speech_with_elevenlabs(input_text=input_text, output_filepath="elevenlabs_testing_autoplay.mp3")
