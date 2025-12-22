# Whisper Transcribe Skill

A Claude Code skill for transcribing audio and video files using OpenAI's Whisper with context-grounding from markdown files.

## Features

- **Audio/Video Transcription**: Convert media files to text using OpenAI Whisper
- **Context Grounding**: Uses markdown files in the same directory to improve accuracy for technical terms, names, and jargon
- **Multi-format Support**: Works with mp3, wav, m4a, mp4, webm, and more
- **Cross-platform**: Supports macOS (Homebrew) and Linux installations

## Prerequisites

### macOS (Homebrew)

```bash
brew install ffmpeg openai-whisper
```

### Linux

```bash
# Install ffmpeg
sudo apt install ffmpeg  # Debian/Ubuntu

# Install Whisper
pip install openai-whisper
```

### Verify Installation

```bash
whisper --version
ffmpeg -version
```

## Usage

### Basic Transcription

```bash
whisper /path/to/audio.mp3 --output_dir /path/to/output
```

### With Context Grounding Script

```bash
python scripts/transcribe_with_context.py /path/to/audio.mp3 --model base --language en
```

The script will:
1. Find markdown context files in the same directory
2. Run Whisper transcription
3. Apply corrections based on context (technical terms, names)
4. Save both original and grounded transcripts

### Model Selection

| Model  | Speed    | Accuracy | RAM Required | Best For                   |
|--------|----------|----------|--------------|----------------------------|
| tiny   | Fastest  | Lower    | ~1 GB        | Quick drafts, testing      |
| base   | Fast     | Good     | ~1 GB        | General use                |
| small  | Medium   | Better   | ~2 GB        | Important recordings       |
| medium | Slower   | High     | ~5 GB        | Professional transcription |
| large  | Slowest  | Highest  | ~10 GB       | Critical accuracy needs    |

## Context Files

Create markdown files in the same directory as your audio to improve transcription accuracy.

### Example Context File

```markdown
# Meeting Context

## Speakers
- Richard Hightower (host)
- Jane Smith (engineering lead)

## Technical Terms
- Kubernetes (container orchestration)
- FastAPI (Python web framework)
- AlloyDB (Google Cloud database)

## Acronyms
- CI/CD - Continuous Integration/Continuous Deployment
- PR - Pull Request
```

See `assets/context-template.md` for a complete template.

## Project Structure

```
whisper-transcribe/
├── SKILL.md                        # Skill definition
├── README.md                       # This file
├── scripts/
│   └── transcribe_with_context.py  # Automated transcription script
├── references/
│   └── whisper-options.md          # Complete Whisper CLI reference
└── assets/
    └── context-template.md         # Template for context files
```

## Triggers

This skill activates when users mention:
- whisper, transcribe, transcription
- audio to text, video to text, speech to text
- meeting transcript, convert recording
- File extensions: .mp3, .wav, .m4a, .mp4, .webm

## License

MIT
