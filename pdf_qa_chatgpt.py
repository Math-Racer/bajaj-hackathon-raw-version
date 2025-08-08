import json
import requests
from pypdf import PdfReader
from openai import OpenAI
import os
import tempfile

def download_pdf(url):
    response = requests.get(url)
    response.raise_for_status()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(response.content)
        return tmp_file.name

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def ask_gpt(context, questions, api_key):
    client = OpenAI(api_key=api_key)
    answers = []
    for question in questions:
        prompt = (
            f"Context: {context}\n\n"
            f"Question: {question}\n"
            "Answer in a brief, conversational, human-like manner, using only one or two sentences. Do not use bullet points, lists, or any formatting. Just give a direct, short answer as if you were talking to a friend.\nAnswer:"
        )
        response = client.responses.create(
            model="gpt-5-nano",
            input=prompt
        )
        answer = response.output_text
        answers.append(answer)
    return answers

def mainfunc(input_json):
    data = json.loads(input_json)
    pdf_url = data["documents"]
    questions = data["questions"]
    from dotenv import load_dotenv
    load_dotenv()  
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    pdf_path = download_pdf(pdf_url)
    context = extract_text_from_pdf(pdf_path)
    answers = ask_gpt(context, questions, api_key)
    return json.dumps({"answers": answers}, indent=2)

# if __name__ == "__main__":
#     # Example usage
#     input_json = '''{
#     "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
#     "questions": [
#         "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?",
#         "What is the waiting period for pre-existing diseases (PED) to be covered?"
#     ]
#     }'''
#     print(main(input_json))
