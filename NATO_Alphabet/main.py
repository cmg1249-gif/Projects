import pandas

nato_df = pandas.read_csv("nato_phonetic_alphabet.csv")
#TODO 1. Create a dictionary in this format:
#{"A": "Alfa", "B": "Bravo"}
nato_dict = {
    row.letter:row.code for (index, row) in nato_df.iterrows()
}
print(nato_dict)
#TODO 2. Create a list of the phonetic code words from a word that the user inputs.
def generate_phonetic():
    user_input = input("Please enter a word: ").upper()
    try:
        coded_word = [nato_dict[letter] for letter in user_input]
    except KeyError:
        print("Invalid input. Please enter a valid word. Letters only")
        generate_phonetic()
    else:
        print(coded_word)

generate_phonetic()