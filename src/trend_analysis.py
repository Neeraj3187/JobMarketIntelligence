from collections import Counter
from src.job_classification import classify_jobs

def get_category_trends():

    df = classify_jobs()

    category_count = Counter(df["Category"])

    return category_count