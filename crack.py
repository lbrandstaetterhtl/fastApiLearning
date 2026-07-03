import decrypt
import analysis

def caesar(text: str, lang: str = 'en') -> list:
    freq_table = analysis.ENGLISH_FREQ if lang == 'en' else analysis.GERMAN_FREQ

    guesses = []
    for shift in range(26):
        guess = decrypt.ceaser(text, shift)
        score = analysis.chi_sq_score(guess, freq_table)
        guesses.append((shift, guess, score))

    guesses.sort(key=lambda x: x[2])

    return guesses