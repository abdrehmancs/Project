import os
import sys
import argparse
from google import genai
from extractor import extract_text_from_pdf

# 1. Initialize the Gemini Client
API_KEY = os.environ.get("GEMINI_API_KEY", "sk-oq2pvQz2LEA17nqhoNohS2mS7nuDYFtAXNBV21Nie0x3xNKd")
client = genai.Client(api_key=API_KEY)

def summarize_with_ai(text):
    """Sends the extracted text to Gemini for an intelligent summary."""
    print("\nSending high-quality extracted text to AI for analysis... Please wait.")

    prompt = (
        "You are an expert document analyst. I have provided text extracted from a PDF "
        "using advanced methods (including table recognition and potential OCR). "
        "Please provide a comprehensive summary of the document. "
        "If there are tables, synthesize the data within them into your summary. "
        "Use clear headings and bullet points for key takeaways:\n\n"
        f"{text}"
    )

    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"Error connecting to AI API: {e}"

def main():
    parser = argparse.ArgumentParser(description="Advanced AI PDF Summarizer")
    parser.add_argument("file", nargs="?", help="Path to the PDF file")
    parser.add_argument("--mode", choices=["simple", "ocr", "hybrid"], default="hybrid",
                        help="Extraction mode: simple (text only), ocr (force OCR), hybrid (text + tables + OCR fallback)")

    args = parser.parse_args()

    file_path = args.file
    if not file_path:
        print("Select your PDF file to summarize with AI...")
        file_path = input("Please enter the path to your PDF file: ").strip('"')

    if not file_path:
        print("No file path provided.")
        return

    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return

    print(f"Using extraction mode: {args.mode}")
    # Extract text using the advanced extractor
    whole_text = extract_text_from_pdf(file_path, mode=args.mode)

    if whole_text and whole_text.strip():
        ai_summary = summarize_with_ai(whole_text)

        print("\n" + "=" * 20 + " ADVANCED AI PDF SUMMARY " + "=" * 20)
        print(ai_summary)
        print("=" * 60)
    else:
        print("Could not extract any readable text from this PDF. Try running with --mode ocr.")

if __name__ == "__main__":
    main()
