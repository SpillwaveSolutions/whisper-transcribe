#!/usr/bin/env python3
"""
Whisper Transcription with Context Grounding

This script automates the full transcription workflow:
1. Find markdown context files in the same directory as the media file
2. Run Whisper transcription
3. Apply context-based corrections to improve accuracy
4. Save the grounded transcript

Usage:
    python transcribe_with_context.py /path/to/audio.mp3 [--model base] [--language en]

Requirements:
    - OpenAI Whisper: brew install openai-whisper (macOS) or pip install openai-whisper
    - ffmpeg: brew install ffmpeg (macOS) or apt install ffmpeg (Linux)
"""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Optional


def find_context_files(media_dir: Path) -> list[Path]:
    """Find all markdown files in the same directory as the media file."""
    return list(media_dir.glob("*.md"))


def extract_terms_from_context(context_files: list[Path]) -> dict[str, str]:
    """
    Extract terminology from context files.
    Returns a dict mapping phonetic variations to correct terms.
    """
    terms = {}

    # Common phonetic misrecognitions and their corrections
    phonetic_mappings = {
        # Technical terms
        "cooler net ease": "Kubernetes",
        "kube er net ease": "Kubernetes",
        "cube er net ease": "Kubernetes",
        "sequel": "SQL",
        "my sequel": "MySQL",
        "post gress": "Postgres",
        "post gray sequel": "PostgreSQL",
        "redis": "Redis",
        "doc er": "Docker",
        "get hub": "GitHub",
        "get lab": "GitLab",
        "jay son": "JSON",
        "yam el": "YAML",
        "rest full": "RESTful",
        "graph cue el": "GraphQL",
        "pie thon": "Python",
        "java script": "JavaScript",
        "type script": "TypeScript",
        "fast a p i": "FastAPI",
        "alloy d b": "AlloyDB",
        "cloud run": "Cloud Run",
        "pub sub": "Pub/Sub",
    }
    terms.update(phonetic_mappings)

    for context_file in context_files:
        try:
            content = context_file.read_text()

            # Extract proper nouns (capitalized words)
            # Look for patterns like "- Name (description)" or "- **Name**"
            name_patterns = [
                r"[-*]\s+\*?\*?([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*)\*?\*?",
                r"##\s+([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*)",
            ]

            for pattern in name_patterns:
                matches = re.findall(pattern, content)
                for name in matches:
                    # Create phonetic variation (lowercase, spaced)
                    phonetic = name.lower().replace("-", " ")
                    terms[phonetic] = name

        except Exception as e:
            print(f"Warning: Could not read context file {context_file}: {e}")

    return terms


def run_whisper(
    media_file: Path,
    output_dir: Path,
    model: str = "base",
    language: Optional[str] = None
) -> Path:
    """Run Whisper transcription on the media file."""

    cmd = [
        "whisper",
        str(media_file),
        "--model", model,
        "--output_dir", str(output_dir),
        "--output_format", "txt",
    ]

    if language:
        cmd.extend(["--language", language])

    print(f"Running Whisper with model '{model}'...")
    print(f"Command: {' '.join(cmd)}")

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running Whisper: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("Error: whisper command not found.")
        print("Install with: brew install openai-whisper (macOS) or pip install openai-whisper")
        sys.exit(1)

    # Find the output file
    output_file = output_dir / f"{media_file.stem}.txt"
    if not output_file.exists():
        print(f"Error: Expected output file not found: {output_file}")
        sys.exit(1)

    return output_file


def apply_context_grounding(transcript: str, terms: dict[str, str]) -> str:
    """Apply context-based corrections to the transcript."""

    grounded = transcript
    corrections_made = []

    for phonetic, correct in terms.items():
        # Case-insensitive replacement
        pattern = re.compile(re.escape(phonetic), re.IGNORECASE)
        if pattern.search(grounded):
            grounded = pattern.sub(correct, grounded)
            corrections_made.append(f"'{phonetic}' -> '{correct}'")

    if corrections_made:
        print(f"\nContext corrections applied:")
        for correction in corrections_made:
            print(f"  {correction}")

    return grounded


def main():
    parser = argparse.ArgumentParser(
        description="Transcribe audio/video with context grounding"
    )
    parser.add_argument(
        "media_file",
        type=Path,
        help="Path to the audio or video file to transcribe"
    )
    parser.add_argument(
        "--model",
        default="base",
        choices=["tiny", "base", "small", "medium", "large"],
        help="Whisper model to use (default: base)"
    )
    parser.add_argument(
        "--language",
        default=None,
        help="Language code (e.g., 'en' for English)"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Output directory (default: same as media file)"
    )

    args = parser.parse_args()

    # Validate input file
    media_file = args.media_file.resolve()
    if not media_file.exists():
        print(f"Error: Media file not found: {media_file}")
        sys.exit(1)

    media_dir = media_file.parent
    output_dir = args.output_dir or media_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Transcribing: {media_file}")
    print(f"Output directory: {output_dir}")

    # Step 1: Find context files
    context_files = find_context_files(media_dir)
    if context_files:
        print(f"\nFound {len(context_files)} context file(s):")
        for cf in context_files:
            print(f"  - {cf.name}")
    else:
        print("\nNo context files found. Proceeding without grounding.")

    # Step 2: Extract terms from context
    terms = extract_terms_from_context(context_files)
    print(f"Loaded {len(terms)} terms for context grounding")

    # Step 3: Run Whisper
    transcript_file = run_whisper(
        media_file,
        output_dir,
        model=args.model,
        language=args.language
    )

    # Step 4: Read transcript
    transcript = transcript_file.read_text()
    print(f"\nTranscript length: {len(transcript)} characters")

    # Step 5: Apply context grounding
    grounded_transcript = apply_context_grounding(transcript, terms)

    # Step 6: Save grounded transcript
    grounded_file = output_dir / f"{media_file.stem}_grounded.txt"
    grounded_file.write_text(grounded_transcript)

    print(f"\n✓ Original transcript: {transcript_file}")
    print(f"✓ Grounded transcript: {grounded_file}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
