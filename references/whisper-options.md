# Whisper CLI Complete Reference

OpenAI Whisper command-line interface options and usage patterns.

## Basic Syntax

```bash
whisper <audio_file> [options]
```

## Core Options

### Model Selection (`--model`)

| Model    | Parameters | Size    | Required VRAM | Relative Speed |
|----------|------------|---------|---------------|----------------|
| tiny     | 39 M       | ~75 MB  | ~1 GB         | ~32x           |
| tiny.en  | 39 M       | ~75 MB  | ~1 GB         | ~32x           |
| base     | 74 M       | ~150 MB | ~1 GB         | ~16x           |
| base.en  | 74 M       | ~150 MB | ~1 GB         | ~16x           |
| small    | 244 M      | ~500 MB | ~2 GB         | ~6x            |
| small.en | 244 M      | ~500 MB | ~2 GB         | ~6x            |
| medium   | 769 M      | ~1.5 GB | ~5 GB         | ~2x            |
| medium.en| 769 M      | ~1.5 GB | ~5 GB         | ~2x            |
| large    | 1550 M     | ~3 GB   | ~10 GB        | 1x             |
| large-v2 | 1550 M     | ~3 GB   | ~10 GB        | 1x             |
| large-v3 | 1550 M     | ~3 GB   | ~10 GB        | 1x             |

**Note:** `.en` models are English-only and perform better for English audio.

```bash
# Examples
whisper audio.mp3 --model tiny      # Fastest, least accurate
whisper audio.mp3 --model base      # Good balance
whisper audio.mp3 --model small     # Better accuracy
whisper audio.mp3 --model medium    # High accuracy
whisper audio.mp3 --model large-v3  # Best accuracy
```

### Language (`--language`)

Force a specific language instead of auto-detection:

```bash
whisper audio.mp3 --language en     # English
whisper audio.mp3 --language es     # Spanish
whisper audio.mp3 --language fr     # French
whisper audio.mp3 --language de     # German
whisper audio.mp3 --language ja     # Japanese
whisper audio.mp3 --language zh     # Chinese
```

Common language codes: `en`, `es`, `fr`, `de`, `it`, `pt`, `ja`, `ko`, `zh`, `ru`, `ar`, `hi`

### Output Format (`--output_format`)

```bash
whisper audio.mp3 --output_format txt   # Plain text (default)
whisper audio.mp3 --output_format vtt   # WebVTT subtitles
whisper audio.mp3 --output_format srt   # SRT subtitles
whisper audio.mp3 --output_format tsv   # Tab-separated values
whisper audio.mp3 --output_format json  # Detailed JSON with timestamps
whisper audio.mp3 --output_format all   # All formats
```

### Output Directory (`--output_dir`)

```bash
whisper audio.mp3 --output_dir ./transcripts
whisper audio.mp3 --output_dir /path/to/output
```

## Advanced Options

### Task (`--task`)

```bash
whisper audio.mp3 --task transcribe   # Transcribe in original language (default)
whisper audio.mp3 --task translate    # Translate to English
```

### Temperature (`--temperature`)

Controls randomness in decoding (0.0-1.0):

```bash
whisper audio.mp3 --temperature 0     # Deterministic
whisper audio.mp3 --temperature 0.2   # Low randomness (default)
```

### Word Timestamps (`--word_timestamps`)

Enable word-level timing information:

```bash
whisper audio.mp3 --word_timestamps True --output_format json
```

### Initial Prompt (`--initial_prompt`)

Provide context to guide transcription style:

```bash
whisper audio.mp3 --initial_prompt "This is a technical discussion about Kubernetes and Docker."
```

### Condition on Previous Text (`--condition_on_previous_text`)

```bash
whisper audio.mp3 --condition_on_previous_text True   # Use context (default)
whisper audio.mp3 --condition_on_previous_text False  # Independent segments
```

### Compression Ratio Threshold (`--compression_ratio_threshold`)

Filter out segments with high compression (likely garbage):

```bash
whisper audio.mp3 --compression_ratio_threshold 2.4
```

### No Speech Threshold (`--no_speech_threshold`)

Probability threshold for silence detection:

```bash
whisper audio.mp3 --no_speech_threshold 0.6
```

### Hallucination Silence Threshold (`--hallucination_silence_threshold`)

Skip silent segments to reduce hallucinations:

```bash
whisper audio.mp3 --hallucination_silence_threshold 2
```

## Performance Options

### Device (`--device`)

```bash
whisper audio.mp3 --device cpu    # CPU only
whisper audio.mp3 --device cuda   # NVIDIA GPU
whisper audio.mp3 --device mps    # Apple Silicon (M1/M2/M3)
```

### Threads (`--threads`)

CPU threads for computation:

```bash
whisper audio.mp3 --threads 4
```

### FP16 (`--fp16`)

Half-precision (faster on GPU):

```bash
whisper audio.mp3 --fp16 True     # Enable (default on GPU)
whisper audio.mp3 --fp16 False    # Disable (required on CPU)
```

## Common Workflows

### Quick Draft Transcription

```bash
whisper meeting.mp3 --model tiny --output_format txt
```

### High-Quality Transcription

```bash
whisper interview.mp3 --model medium --language en --output_format all
```

### Generate Subtitles

```bash
whisper video.mp4 --model small --output_format srt
```

### Translate Foreign Audio to English

```bash
whisper spanish_audio.mp3 --task translate --model medium
```

### Technical Content with Context

```bash
whisper tech_talk.mp3 \
  --model medium \
  --language en \
  --initial_prompt "Technical discussion about cloud computing, Kubernetes, and microservices architecture." \
  --output_format json
```

### Batch Processing

```bash
# Transcribe all MP3 files in a directory
for f in *.mp3; do
  whisper "$f" --model base --output_dir ./transcripts
done
```

## Supported Audio Formats

Whisper uses ffmpeg and supports:
- **Audio**: mp3, wav, m4a, flac, ogg, opus, wma, aac
- **Video**: mp4, mkv, webm, avi, mov (extracts audio automatically)

## Error Handling

### Out of Memory

```bash
# Use smaller model
whisper audio.mp3 --model tiny

# Or disable FP16 on CPU
whisper audio.mp3 --device cpu --fp16 False
```

### Slow Performance

```bash
# Use faster model
whisper audio.mp3 --model base

# Specify device explicitly
whisper audio.mp3 --device mps  # Apple Silicon
```

### Poor Accuracy

```bash
# Use larger model
whisper audio.mp3 --model medium

# Specify language explicitly
whisper audio.mp3 --language en

# Provide context
whisper audio.mp3 --initial_prompt "Meeting about project planning"
```

## Python API (Alternative)

For programmatic use:

```python
import whisper

model = whisper.load_model("base")
result = model.transcribe("audio.mp3")
print(result["text"])

# With options
result = model.transcribe(
    "audio.mp3",
    language="en",
    task="transcribe",
    fp16=False
)
```

## References

- [OpenAI Whisper GitHub](https://github.com/openai/whisper)
- [Whisper Model Card](https://github.com/openai/whisper/blob/main/model-card.md)
- [Supported Languages](https://github.com/openai/whisper/blob/main/whisper/tokenizer.py)
