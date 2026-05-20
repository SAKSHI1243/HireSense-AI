QUESTION_BANK = {

    "python": [
        "Explain decorators in Python.",
        "What is list comprehension?",
        "Difference between list and tuple?"
    ],

    "machine learning": [
        "Explain bias vs variance.",
        "What is overfitting?",
        "Difference between bagging and boosting?"
    ],

    "nlp": [
        "Explain TF-IDF.",
        "What are word embeddings?",
        "Difference between stemming and lemmatization?"
    ],

    "sql": [
        "Explain joins in SQL.",
        "Difference between WHERE and HAVING?",
        "What are indexes?"
    ],

    "docker": [
        "What is Docker?",
        "Difference between Docker image and container?",
        "Why use containerization?"
    ]
}
def generate_questions(skills):

    questions = []

    for skill in skills:

        if skill in QUESTION_BANK:
            questions.extend(
                QUESTION_BANK[skill]
            )

    return questions[:10]