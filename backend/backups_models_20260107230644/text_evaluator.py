import textdistance
import Levenshtein

def evaluate_text(student_answer: str, model_answer: str) -> dict:
    similarity = textdistance.cosine.normalized_similarity(student_answer, model_answer)
    levenshtein_ratio = Levenshtein.ratio(student_answer, model_answer)

    return {
        "similarity": similarity,
        "levenshtein_ratio": levenshtein_ratio,
    }