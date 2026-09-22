"""
SIMPLE GENERATIVE AI APP: Text Summarizer (Gemini version)
============================================================

This script lets you paste text or pass a file path, then sends it to Google Gemini
for a short 3-bullet summary.

Setup:
    1. Install dependencies: pip install -r requirements.txt
    2. Copy .env.example to .env and add your API key.
    3. Run the script:
         python simple_summarizer_gemini.py
"""

import os
import sys
from pathlib import Path

from google import genai
from google.genai import types
from dotenv import load_dotenv


load_dotenv()


def get_api_key() -> str:
    """Return the Gemini API key from the environment or local .env file."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or not api_key.strip():
        raise RuntimeError(
            "GEMINI_API_KEY is not set. "
            "Add it to a .env file as GEMINI_API_KEY=your-key-here."
        )
    return api_key.strip()


def summarize_text(text_to_summarize: str) -> str:
    """Send text to Gemini and request a concise 3-bullet summary."""
    client = genai.Client(api_key=get_api_key())

    chat = client.chats.create(
        model="gemini-3.6-flash",
        config=types.GenerateContentConfig(
            system_instruction=(
                "You are a concise summarization assistant. "
                "Return exactly three plain-text lines, each beginning with '- '. "
                "Each line must be under 20 words. Do not add headings, labels, "
                "numbers, markdown emphasis, or commentary."
            ),
            max_output_tokens=300,
            response_mime_type="text/plain",
        ),
    )

    response = chat.send_message(
        message=(
            "Summarize the text below. Return exactly three separate lines. "
            "Each line must start with '- ' and contain one concise fact. "
            "Do not use headings, labels, numbering, asterisks, or any text "
            "before or after the three lines.\n\n"
            f"Text to summarize:\n{text_to_summarize}"
        )
    )

    summary = getattr(response, "text", None)
    if not summary:
        raise RuntimeError("Gemini returned no summary text.")

    bullet_lines = [
        line.strip()
        for line in summary.splitlines()
        if line.strip().startswith("-")
    ]
    if len(bullet_lines) < 3:
        response = chat.send_message(
            message=(
                "Your previous answer had fewer than three bullet points. "
                "Rewrite it as exactly three separate lines, each beginning "
                "with '- '. Do not include any other text."
            )
        )
        summary = getattr(response, "text", None)
        if not summary:
            raise RuntimeError("Gemini returned no summary text.")

    return summary.strip()


def read_input_text() -> str:
    """Read text from CLI input or a file path."""
    if len(sys.argv) > 1:
        arg = sys.argv[1]

        if arg.lower() in {"-h", "--help"}:
            print("Usage: python simple_summarizer_gemini.py [text-or-file-path]")
            print("Examples:")
            print("  python simple_summarizer_gemini.py \"This is my text\"")
            print("  python simple_summarizer_gemini.py my_file.txt")
            sys.exit(0)

        candidate = Path(arg)
        if candidate.exists() and candidate.is_file():
            return candidate.read_text(encoding="utf-8")
        return arg

    print("=" * 50)
    print("SIMPLE AI TEXT SUMMARIZER (Gemini)")
    print("=" * 50)
    print("\nPaste the text you want summarized, then press Enter twice:\n")

    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)

    return "\n".join(lines)


def main():
    user_text = read_input_text().strip()

    if not user_text:
        print("No text entered. Exiting.")
        sys.exit(0)

    print("\nSending your text to Gemini...\n")

    try:
        summary = summarize_text(user_text)
        print("-" * 50)
        print("SUMMARY:")
        print("-" * 50)
        print(summary)
    except Exception as e:
        print(f"Something went wrong: {e}")
        print("\nCheck that:")
        print("  1. You installed the library: pip install -r requirements.txt")
        print("  2. GEMINI_API_KEY is set correctly")
        print("  3. You have an active internet connection")
        sys.exit(1)


if __name__ == "__main__":
    main()
