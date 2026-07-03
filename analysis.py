GERMAN_FREQ = {
    'A': 6.51, 'B': 1.89, 'C': 3.06, 'D': 5.08, 'E': 17.40,
    'F': 1.66, 'G': 3.01, 'H': 4.76, 'I': 7.55, 'J': 0.27,
    'K': 1.21, 'L': 3.44, 'M': 2.53, 'N': 9.78, 'O': 2.51,
    'P': 0.79, 'Q': 0.02, 'R': 7.00, 'S': 7.27, 'T': 6.15,
    'U': 4.35, 'V': 0.67, 'W': 1.89, 'X': 0.03, 'Y': 0.04,
    'Z': 1.13
}

ENGLISH_FREQ = {
    'A': 8.17, 'B': 1.49, 'C': 2.78, 'D': 4.25, 'E': 12.70,
    'F': 2.23, 'G': 2.02, 'H': 6.09, 'I': 6.97, 'J': 0.15,
    'K': 0.77, 'L': 4.03, 'M': 2.41, 'N': 6.75, 'O': 7.51,
    'P': 1.93, 'Q': 0.10, 'R': 5.99, 'S': 6.33, 'T': 9.06,
    'U': 2.76, 'V': 0.98, 'W': 2.36, 'X': 0.15, 'Y': 1.97,
    'Z': 0.07
}

def chi_sq_score(text: str, expected_freq: dict) -> float:
    letters = [char.upper() for char in text if char.isalpha()]
    length = len(letters)

    if length == 0:
        return float('inf')

    observed_freq = {chr(i): 0 for i in range(ord('A'), ord('Z')+1)}

    for letter in letters:
        observed_freq[letter] += 1

    chi_score = 0.0

    for letter in observed_freq:
        observed_percent = (observed_freq[letter] / length) * 100
        expected_percent = expected_freq[letter]
        chi_score += ((observed_percent - expected_percent) ** 2) / expected_percent

    return chi_score

def confidence_score(guesses: list) -> dict:
    if len(guesses) < 2:
        return {'level': 'unknown', 'ratio': 0.0, "message": "Not enough guesses to determine confidence."}

    best_score = guesses[0][2]
    second_best_score = guesses[1][2]

    if best_score == 0:
        return {'level': 'unknown', 'ratio': 0.0, 'message': "Second best score is zero, cannot compute confidence."}

    ratio = second_best_score / best_score

    if ratio > 2.0:
        return {'level': 'high', 'ratio': ratio, 'message': "High confidence in the best guess."}
    elif ratio > 1.5:
        return {'level': 'medium', 'ratio': ratio, 'message': "Medium confidence in the best guess."}
    else:
        return {'level': 'low', 'ratio': ratio, 'message': "Low confidence in the best guess."}