import os
import glob
import time
import re
from symspellpy import SymSpell, Verbosity

STT_PATH = "./files/raw_transcriptions/"
SPELLCHECK_PATH = "./files/spellchecked_transcriptions/"

sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)

dictionary_path = "./files/pt_br_full.txt"
sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1, encoding="utf-8")

def get_timestamp(input_file):
    timestamp = re.search(r'(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})', input_file).group(1)
    return timestamp

def correct_text_file(input_file):
    timestamp = get_timestamp(input_file)
    output_file = os.path.join(SPELLCHECK_PATH, f"transcription_{timestamp}.txt" )

    with open(input_file, "r", encoding="windows-1252") as infile, open(output_file, "w", encoding="utf-8") as outfile:
        for line in infile:
            words = line.split()
            corrected_words = [sym_spell.lookup(word, Verbosity.CLOSEST, max_edit_distance=2)[0].term if sym_spell.lookup(word, Verbosity.CLOSEST, max_edit_distance=2) else word for word in words]
            corrected_line = " ".join(corrected_words)
            outfile.write(corrected_line + "\n")
    return output_file

if __name__ == "__main__":
    input_txt = "./files/transcription.txt"
    output_txt = correct_text_file(input_txt)

    print(f"Corrected text saved to {output_txt}")
