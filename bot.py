import os
import json
from google import genai

API_KEY = os.environ.get('GEMINI_API_KEY')
if not API_KEY:
    raise SystemExit('GEMINI_API_KEY not set')

client = genai.Client()

base = os.path.dirname(__file__)
data_dir = os.path.join(base, 'data')

with open(os.path.join(base, 'system_prompt.json'), 'r', encoding='utf-8') as f:
    system_prompt = json.load(f)['prompt']

files = [
    'citizen_writer_349A.json',
    'aditya_das_promenade.json',
    'senior_sid_dubey_renewing_standards.json',
    'tweets.json',
    'glossary.json'
]

examples = []
for fn in files:
    p = os.path.join(data_dir, fn)
    if not os.path.exists(p):
        continue
    with open(p, 'r', encoding='utf-8') as f:
        try:
            j = json.load(f)
        except Exception:
            continue
    examples.append({ 'filename': fn, 'content': j })

prompt = {
    'system': system_prompt,
    'task': 'Analyze selected text and return JSON according to system prompt',
    'data_files': examples
}

text_to_analyze = None
if os.path.exists('selected.txt'):
    with open('selected.txt', 'r', encoding='utf-8') as f:
        text_to_analyze = f.read().strip()

if not text_to_analyze:
    text_to_analyze = input('Paste the text to analyze: ').strip()

payload = {
    'model': 'gemini-2.5-flash',
    'contents': f"{system_prompt}\n\nText:\n{text_to_analyze}",
}

response = client.models.generate_content(
    model=payload['model'],
    contents=payload['contents'],
)

print(response.text)
