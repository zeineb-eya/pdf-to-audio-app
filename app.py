from flask import Flask, request, send_file, render_template, after_this_request
import PyPDF2
from gtts import gTTS
import os
import asyncio
import time 

app = Flask(__name__)

if not os.path.exists('uploads'):
    os.makedirs('uploads')

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text

def text_to_speech(text, lang, output_file):
    tts = gTTS(text=text, lang=lang)
    tts.save(output_file)

async def process_pdf(pdf_path):
    time.sleep(5)
    arabic_text = extract_text_from_pdf(pdf_path)
    audio_output = 'output_audio.mp3'
    text_to_speech(arabic_text, 'ar', audio_output)
    return audio_output
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file uploaded", 400
        
        file = request.files['file']
        if file.filename == '':
            return "No file selected", 400
        
        pdf_path = os.path.join('uploads', file.filename)
        file.save(pdf_path)
        
        audio_file = asyncio.run(process_pdf(pdf_path))
        
        @after_this_request
        def cleanup(response):
            try:
                os.remove(pdf_path)
                os.remove(audio_file)
            except Exception as e:
                app.logger.error(f"Error cleaning up files: {e}")
            return response
        
        return send_file(audio_file, as_attachment=True)
    
    return render_template('index.html')

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
