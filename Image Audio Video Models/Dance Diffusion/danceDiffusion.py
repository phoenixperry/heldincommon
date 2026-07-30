"""
Dance Diffusion (Harmonai) — Unconditional Audio Generation
Requirements:
    pip install diffusers==0.27.2 huggingface_hub==0.23.4 accelerate torch scipy --break-system-packages

Available pretrained checkpoints (swap MODEL_ID to try others):
    "harmonai/glitch-440k"        - glitch/electronic textures
    "harmonai/jmann-large-580k"   - long-form music
    "harmonai/maestro-150k"       - piano (trained on MAESTRO dataset)
    "harmonai/unlocked-250k"      - "Unlocked Recordings" archival audio
    "harmonai/honk-140k"          - car horn / honk sounds (fun demo checkpoint)
"""

import torch
import scipy.io.wavfile
from diffusers import DiffusionPipeline

MODEL_ID = "harmonai/glitch-440k"
NUM_SAMPLES = 1
AUDIO_LENGTH_SECONDS = 4  # model-dependent; longer = more inference steps needed
SEED = 42

def main():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    generator = torch.manual_seed(SEED)

    pipe = DiffusionPipeline.from_pretrained(MODEL_ID)
    pipe = pipe.to(device)

    audios = pipe(audio_length_in_s=AUDIO_LENGTH_SECONDS, num_inference_steps=100, generator=generator, batch_size=NUM_SAMPLES).audios

    for i, audio in enumerate(audios):
        out_path = f"dance_diffusion_output_{i}.wav"
        scipy.io.wavfile.write(out_path, pipe.unet.sample_rate, audio.transpose())
        print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()