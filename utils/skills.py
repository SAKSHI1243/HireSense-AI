SKILLS = [

    "python",
    "sql",
    "java",
    "javascript",
    "machine learning",
    "deep learning",
    "nlp",
    "pandas",
    "numpy",
    "scikit learn",
    "tensorflow",
    "keras",
    "docker",
    "flask",
    "fastapi",
    "git",
    "tableau",
    "power bi",
    "opencv",
    "kafka",
    "mongodb",
    "mysql",
    "postgresql",
    "aws",
    "azure"
]
def extract_skills(text):

    found_skills = []

    for skill in SKILLS:

        if skill.lower() in text:
            found_skills.append(skill)

    return list(set(found_skills))