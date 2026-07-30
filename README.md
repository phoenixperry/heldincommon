# Open-Source AI Model Landscape

A static reference site cataloguing open-source image, video, and audio generation models — covering license type, training data provenance, attribution mechanisms, commercial-use terms, and known data/IP gaps for each model.

Built for the Federated Data Commons for Creative Communities (FDCCC) project at NYU.

## Site

Plain HTML/CSS/JS, no build step or framework:

- [`index.html`](index.html) — page structure
- [`styles1.css`](styles1.css) — styling
- [`script.js`](script.js) — search, filtering, sorting, and modal logic
- [`data.js`](data.js) — the model dataset, as a `MODELS` array

## Adding a model

Append an object to `MODELS` in `data.js` following the existing field structure, then commit and push — GitHub Pages picks up the change automatically.

All fields:

```js
{
  model: "Model Name",
  developer: "Developer",
  year: "2024",
  modality: "Image" | "Video" | "Audio",
  io: "Text → Image",
  licenseType: "Fully Open" | "Permissive" | "Restricted-Open" | "Mixed",
  licenseName: "Apache 2.0",
  dataDisclosed: "Full" | "Partial" | "No",
  dataSources: "...",
  attribution: "...",
  commercialUse: "Full" | "Yes" | "Partial" | "No",
  finetune: "Yes" | "Partial" | "No",
  checkpoint: "Yes" | "No",
  api: "Yes" | "No",
  exportFormat: "PNG, JPG",
  openSource: "Yes" | "No",
  dataGap: "...",
  notes: "..."
}
```

## Adding a ComfyUI workflow / output

To attach a workflow and/or output sample to a model's detail view, place the files in a subfolder under `Image Audio Video Models/`:

```
Image Audio Video Models/
  Your Model Name/
    workflow.json              ← ComfyUI workflow export (optional)
    output.png / .wav / .mp4  ← example output (optional)
```

Then add a `workflow` field to the model's entry in `data.js`. All sub-fields are optional — include only what you have:

```js
workflow: {
  folder: "Your Model Name",   // must match folder name exactly
  json:   "workflow.json",     // ComfyUI workflow — shows Workflow JSON tab
  image:  "output.png",        // image output   ─┐
  audio:  "output.wav",        // audio output    ├ shows Output tab (use one)
  video:  "output.mp4"         // video output   ─┘
}
```

The modal will show an **Output** tab (image viewer, audio player, or video player) and/or a **Workflow JSON** tab depending on what fields are present. Models with no `workflow` field show only the Details tab.

> **Note:** if a model folder contains a Python virtual environment (`.venv/`), it is gitignored automatically — do not commit it.

## Running locally

Any static file server works, e.g.:

```
python -m http.server 8080
```

Then open `http://localhost:8080`.

## Hosting

Served via GitHub Pages from this repo.
