from tkinter import filedialog, Tk
from google import genai
from google.genai import types
from pypdf import PdfReader

# 1. Initialize the Gemini Client with your free API key
# Replace with your actual key from Google AI Studio
API_KEY = "sk-oq2pvQz2LEA17nqhoNohS2mS7nuDYFtAXNBV21Nie0x3xNKd"
client = genai.Client(api_key=API_KEY)


def summarize_with_ai(text):
    """Sends the extracted text to Gemini for an intelligent summary."""
    print("\nSending text to AI for analysis... Please wait.")

    prompt = (
        "You are an expert document assistant. Provide a concise, clear summary "
        "of the following text. Use bullet points for key takeaways if helpful:\n\n"
        f"{text}"
    )

    try:
        # Using the fast, free tier model
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"Error connecting to AI API: {e}"


# --- Main Program Layout ---

# Hide the main blank Tkinter window
root = Tk()
root.withdraw()

print("Select your PDF file to summarize with AI...")
file_path = filedialog.askopenfilename(
    title="Select a PDF file", filetypes=[("PDF Files", "*.pdf")]
)

if file_path:
    # Extract text from the PDF
    reader = PdfReader(file_path)
    whole_text = ""
    for page in reader.pages:
        whole_text += page.extract_text() + "\n"

    # Ensure we actually extracted text before calling the AI
    if whole_text.strip():
        # Trim text slightly if it's an incredibly massive book, though flash handles up to 1M tokens
        ai_summary = summarize_with_ai(whole_text)

        print("\n" + "=" * 20 + " AI PDF SUMMARY " + "=" * 20)
        print(ai_summary)
        print("=" * 56)
    else:
        print("Could not extract any readable text from this PDF.")
else:
    print("No file was selected.")
