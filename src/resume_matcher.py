from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_similarity(resume_text, jobs_df):
    model = SentenceTransformer(
        "all-MiniLM-L6-v2"
    )

    job_texts = []

    for _, row in jobs_df.iterrows():

        job_text = (
            str(row["JobTitle"]) + " " +
            str(row["Skills"])
        )

        job_texts.append(job_text)

    resume_embedding = model.encode(
        [resume_text]
    )

    job_embeddings = model.encode(
        job_texts
    )

    similarities = cosine_similarity(
        resume_embedding,
        job_embeddings
    )[0]

    return similarities

def get_missing_skills(
    resume_text,
    job_skills
):

    valid_skills = {
        "python",
        "sql",
        "aws",
        "docker",
        "kubernetes",
        "linux",
        "java",
        "javascript",
        "react",
        "node",
        "machine learning",
        "data science",
        "pandas",
        "numpy",
        "tensorflow",
        "pytorch",
        "git",
        "github",
        "azure",
        "devops",
        "cybersecurity",
        "jira",
        "mongodb",
        "mysql",
        "postgresql"
    }

    resume_text = resume_text.lower()

    skills = [
        skill.strip().lower()
        for skill in str(job_skills).split(",")
    ]

    missing = []

    for skill in skills:

        if (
            skill in valid_skills
            and skill not in resume_text
        ):
            missing.append(skill)

    return missing


def calculate_resume_score(
    resume_text,
    missing_skills
):

    score = 100 - (len(missing_skills) * 10)

    if score < 0:
        score = 0

    return score


def get_resume_feedback(score):

    if score >= 80:
        return "Excellent Resume"

    elif score >= 60:
        return "Good Resume"

    elif score >= 40:
        return "Average Resume"

    else:
        return "Needs Improvement"


def recommend_career(resume_text):

    text = resume_text.lower()

    if "machine learning" in text:
        return "AI / Machine Learning Engineer"

    elif "sql" in text and "python" in text:
        return "Data Analyst"

    elif "aws" in text or "docker" in text:
        return "DevOps Engineer"

    elif "react" in text or "javascript" in text:
        return "Frontend Developer"

    else:
        return "Software Engineer"
def calculate_jd_match(
    resume_text,
    job_description
):

    model = SentenceTransformer(
        "all-MiniLM-L6-v2"
    )

    embeddings = model.encode(
        [resume_text, job_description]
    )

    similarity = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )[0][0]

    return round(
        similarity * 100,
        2
    )
def get_jd_missing_skills(
    resume_text,
    job_description
):

    valid_skills = {
        "python",
        "sql",
        "aws",
        "docker",
        "kubernetes",
        "linux",
        "java",
        "javascript",
        "react",
        "node",
        "machine learning",
        "data science",
        "pandas",
        "numpy",
        "tensorflow",
        "pytorch",
        "git",
        "github",
        "azure",
        "devops",
        "cybersecurity",
        "jira",
        "mongodb",
        "mysql",
        "postgresql"
    }

    resume_text = resume_text.lower()
    job_description = job_description.lower()

    missing = []

    for skill in valid_skills:

        if (
            skill in job_description
            and skill not in resume_text
        ):
            missing.append(skill)

    return sorted(missing)