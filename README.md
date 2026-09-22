# Simple Summary Text Generator

A small Python app that sends input text to Google Gemini and returns a short 3-bullet summary.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set your Gemini API key:
   ```bash
   # Windows Command Prompt
   copy .env.example .env
   notepad .env
   ```
   Replace `your-key-here` in `.env` with your Gemini API key, then save the file.
   The application loads `.env` automatically when it starts.
3. Run the app:
   ```bash
   python simple_summarizer_gemini.py
   ```

You can also pass a string directly or a file path as a command-line argument.

## Example

```bash
python simple_summarizer_gemini.py "This project builds a simple text summarizer using Gemini."
```
