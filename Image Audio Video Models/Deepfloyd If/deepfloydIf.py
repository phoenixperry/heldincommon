"""
DeepFloyd IF — Text-to-Image (pixel-space cascade diffusion)
Requirements:
    pip install diffusers accelerate transformers==5.14.1 sentencepiece protobuf tiktoken torch --break-system-packages

IMPORTANT — Gated model:
    1. Accept the license at https://huggingface.co/DeepFloyd/IF-I-XL-v1.0
    2. Log in via: hf auth login (paste an HF access token)
    Research-only license — no commercial use.

VRAM note: Stage I (XL) + Stage II + Stage III need ~16GB+ combined.
Use the "-M" (medium) or "-L" (large, not XL) variants below if VRAM-limited.
"""

import torch
from diffusers import DiffusionPipeline
from diffusers.utils import pt_to_pil
 
PROMPT = "a photograph of a cozy cabin in a snowy forest, warm light in the windows, high detail"
NEGATIVE_PROMPT = "blurry, low quality, distorted, watermark"
SEED = 42
 
def main():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    generator = torch.manual_seed(SEED)
 
    # Stage 1: base 64x64 pixel-space diffusion
    # safety_checker=None avoids a known transformers-v5 / diffusers-0.39 incompatibility
    # in DeepFloyd's IFSafetyChecker class (missing all_tied_weights_keys attribute).
    stage_1 = DiffusionPipeline.from_pretrained("DeepFloyd/IF-I-XL-v1.0", variant="fp16", torch_dtype=torch.float16, safety_checker=None, feature_extractor=None, requires_safety_checker=False)
    if device == "cuda":
        stage_1.enable_model_cpu_offload()
    else:
        stage_1.to(device)
 
    prompt_embeds, negative_embeds = stage_1.encode_prompt(PROMPT, negative_prompt=NEGATIVE_PROMPT)
 
    image = stage_1(prompt_embeds=prompt_embeds, negative_prompt_embeds=negative_embeds, generator=generator, output_type="pt").images
 
    # Stage 2: 64x64 -> 256x256 super-resolution
    stage_2 = DiffusionPipeline.from_pretrained("DeepFloyd/IF-II-L-v1.0", text_encoder=None, variant="fp16", torch_dtype=torch.float16, safety_checker=None, feature_extractor=None, requires_safety_checker=False)
    if device == "cuda":
        stage_2.enable_model_cpu_offload()
    else:
        stage_2.to(device)
 
    image = stage_2(image=image, prompt_embeds=prompt_embeds, negative_prompt_embeds=negative_embeds, generator=generator, output_type="pt").images
 
    # Stage 3: 256x256 -> 1024x1024 super-resolution (Stable Diffusion x4 upscaler)
    stage_3 = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-x4-upscaler", safety_checker=None, feature_extractor=None, watermarker=None, requires_safety_checker=False, torch_dtype=torch.float16)
    if device == "cuda":
        stage_3.enable_model_cpu_offload()
    else:
        stage_3.to(device)
 
    final_image = stage_3(prompt=PROMPT, image=image, noise_level=100, generator=generator).images
 
    final_image[0].save("deepfloyd_if_output.png")
    print("Saved: deepfloyd_if_output.png")
 
 
if __name__ == "__main__":
    main()