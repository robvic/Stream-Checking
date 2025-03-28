import os
import glob
import time
import re
from openai import OpenAI

SPELLCHECK_PATH = "./files/spellchecked_transcriptions"
CORRECTED_PATH = "./files/corrected_transcriptions/"

INSTRUCTION = """
Corrija o seguinte texto em casos onde a palavra possa estar mal escrita ou mal compreendida, para a palavra ou expressão mais próxima que mantenha a coerência geral do texto.
Responda apenas com o texto corrigido.

Texto:

"""

def get_timestamp(input_file):
    timestamp = re.search(r'(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})', input_file).group(1)
    return timestamp

def correct_text(input_file):
    timestamp = get_timestamp(input_file)
    output_file = os.path.join(CORRECTED_PATH, f"transcription_{timestamp}.txt" )

    with open(input_file, 'r') as f:
        text = f.read()

    client = OpenAI(api_key=os.environ.get("GPT_KEY"))

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[{
            "role": "user",
            "content": INSTRUCTION + text
        }]
    )

    content =  completion.choices[0].message.content

    with open(output_file, 'w+') as f:
        f.write(content)
    
    return output_file

if __name__ == "__main__":
    initial_time = time.time()
    files = glob.glob(os.path.join(SPELLCHECK_PATH, '*.txt'))
    for file in files:
        output_file = correct_text(file)
        print(f"Corrected text saved to {output_file}")
    duration = time.time() - initial_time
    print(f"Took {duration} to process files.")
