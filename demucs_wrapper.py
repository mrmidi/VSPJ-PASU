import torch
import torchaudio
from torchaudio.pipelines import HDEMUCS_HIGH_MUSDB_PLUS
from torchaudio.transforms import Fade
from matplotlib import pyplot as plt


bundle = HDEMUCS_HIGH_MUSDB_PLUS # HDEMUCS_HIGH_MUSDB_PLUS
# check if cuda is available
if torch.cuda.is_available():
    print("CUDA is available")
    device = torch.device("cuda:0")
else:
    print("CUDA is not available")
    device = torch.device("cpu")

model = bundle.get_model().to(device)
sample_rate = bundle.sample_rate # 44100
print(f"Sample rate: {sample_rate}")

def separate_sources(audio_path):
    print("Processing audio...")
    waveform, _ = torchaudio.load(audio_path, normalize=True) #  loads and normalizes the audio file
    waveform = waveform.to(device) # send to device

    # parameters
    segment: int = 10  # segment length in seconds
    overlap = 0.1  # overlap ratio between segments

    # Apply the model to the mixture
    sources = apply_model(
        model,
        waveform.unsqueeze(0),
        segment=segment,
        overlap=overlap,
    )[0]

    sources_list = model.sources  # ['vocals', 'drums', 'bass', 'other']
    sources = list(sources)  # convert to list

    return dict(zip(sources_list, sources))  # return dictionary of sources

def apply_model(
        model,
        mix,
        segment=10.0,
        overlap=0.1,
):
    batch, channels, length = mix.shape  # create batch, channels, length based on mix shape

    chunk_len = int(sample_rate * segment * (1 + overlap))  # define chunk_len

    start = 0
    end = chunk_len
    overlap_frames = overlap * sample_rate  # define overlap_frames. overlap is 0.1, sample_rate is 44100
    fade = Fade(fade_in_len=0, fade_out_len=int(overlap_frames), fade_shape="linear")  # create fade object

    final = torch.zeros(batch, len(model.sources), channels, length, device=device)  # create final tensor

    # loop through mix and apply model
    while start < length - overlap_frames:
        # it's possible to send websocket messages here to update the progress bar
        print(f"Processing chunk {start} to {end} of {length}...")
        chunk = mix[:, :, start:end]
        with torch.no_grad():
            out = model.forward(chunk)
        out = fade(out)
        final[:, :, :, start:end] += out
        if start == 0:
            fade.fade_in_len = int(overlap_frames)
            start += int(chunk_len - overlap_frames)
        else:
            start += chunk_len
        end += chunk_len
        if end >= length:
            fade.fade_out_len = 0
    return final

def get_spectrograms(sources):
    spec_transform = torchaudio.transforms.Spectrogram(n_fft=400, hop_length=160)
    spectrograms = {}
    files = {}

    for source, audio in sources.items():
        spectrogram = spec_transform(audio)
        spectrograms[source] = spectrogram
        file = plot_spectrogram(spectrogram, source)
        files[source] = file
    return files

def plot_spectrogram(spectrogram, title):
    num_channels = spectrogram.shape[0]
    for channel in range(num_channels):
        fig, ax = plt.subplots()
        cax = ax.matshow(20 * spectrogram[channel].log2(), origin='lower', aspect='auto', cmap=plt.cm.inferno)
        fig.colorbar(cax)
        plt.title(f'Spectrogram for {title} Channel {channel+1}')
        file = f'static/{title}_channel_{channel+1}.png'
        plt.savefig(file)
        plt.close(fig)  # Close the figure after saving to free up memory
    return file

# simple function to save audio files. returns dictionary of files
def get_audio_files(sources):
    files = {}
    for source, audio in sources.items():
        file = f'static/{source}.wav'
        torchaudio.save(file, audio, sample_rate=sample_rate)
        files[source] = file
    return files
