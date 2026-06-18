import requests
import pandas as pd


def fetch_jsearch_jobs():

    url = "https://jsearch.p.rapidapi.com/search"

    queries = [
        "python developer",
        "software engineer",
        "data analyst",
        "data scientist",
        "machine learning engineer",
        "ai engineer",
        "devops engineer",
        "cloud engineer",
        "backend developer",
        "frontend developer",
        "full stack developer"
    ]

    headers = {
        "X-RapidAPI-Key": "775aa0e137msh02bbbe8176ae57fp1b6832jsn36384b64b1a8",
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }

    all_jobs = []

    for q in queries:

        print("Fetching:", q)

        try:

            response = requests.get(
                url,
                headers=headers,
                params={
                    "query": q,
                    "page": "1",
                    "num_pages": "2"
                },
                timeout=30
            )

            data = response.json()

            for job in data.get("data", []):

                all_jobs.append({
                    "JobTitle": job.get("job_title", ""),
                    "Company": job.get("employer_name", ""),
                    "Location": job.get("job_city", ""),
                    "Skills": "",
                    "JobLink": job.get("job_apply_link", ""),
                    "Source": "JSearch"
                })

        except Exception as e:
            print("Error:", e)

    df = pd.DataFrame(all_jobs)

    df.drop_duplicates(
        subset=["JobTitle", "Company"],
        inplace=True
    )

    print("Total JSearch Jobs:", len(df))

    return df