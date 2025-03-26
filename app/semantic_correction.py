import os
from openai import OpenAI

INPUT_FILE = "./files/transcription_spellchecked.txt"
OUTPUT_FILE = "./files/transcription_corrected.txt"
INSTRUCTION = """
Corrija o seguinte texto em casos onde a palavra possa estar mal escrita ou mal compreendida, para a palavra ou expressão mais próxima que mantenha a coerência geral do texto.

Texto:

"""

def read_file(file=INPUT_FILE):
    with open(file, 'r') as f:
        text = f.read()
    return text

def send_message(text):
    client = OpenAI(api_key=os.environ.get("GPT_KEY"))

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[{
            "role": "user",
            "content": INSTRUCTION + text
        }]
    )

    return completion.choices[0].message.content

def write_file(text, file=OUTPUT_FILE):
    with open(file, 'w+') as f:
        f.write(text)

if __name__ == "__main__":
    text = read_file()
    response = send_message(text)
    write_file(response)

