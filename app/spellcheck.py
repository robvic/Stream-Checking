from symspellpy import SymSpell, Verbosity

sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)

dictionary_path = "../files/pt_br_full.txt"
sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)

def correct_text_file(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", encoding="utf-8") as outfile:
        for line in infile:
            words = line.split()
            corrected_words = [sym_spell.lookup(word, Verbosity.CLOSEST, max_edit_distance=2)[0].term if sym_spell.lookup(word, Verbosity.CLOSEST, max_edit_distance=2) else word for word in words]
            corrected_line = " ".join(corrected_words)
            outfile.write(corrected_line + "\n")

if __name__ == "__main__":
    input_txt = "./files/transcription.txt"
    output_txt = "./files/transcription_spellchecked.txt"
    correct_text_file(input_txt, output_txt)

    print(f"Corrected text saved to {output_txt}")
