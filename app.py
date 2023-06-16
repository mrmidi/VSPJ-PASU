from flask import Flask, request, render_template
import demucs_wrapper
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = os.path.join('uploads', file.filename)
            file.save(filename)
            sources = demucs_wrapper.separate_sources(filename)
            spectrograms = demucs_wrapper.get_spectrograms(sources)
            audio_files = demucs_wrapper.get_audio_files(sources)
            results = []
            for source in sources:
                results.append({
                    "source": source,
                    "spectrogram": spectrograms[source],
                    "audio_file": audio_files[source],
                })
            return render_template('results.html', results=results)
    # check if static folder exists
    if not os.path.exists('static'):
        os.makedirs('static')
    # check if uploads folder exists
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
