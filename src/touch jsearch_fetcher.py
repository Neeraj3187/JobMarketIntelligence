import requests
import pandas as pd


def fetch_jsearch_jobs():

    url = "https://jsearch.p.rapidapi.com/search"

    querystring = {
        "query": "software developer",
        "page": "1",
        "num_pages": "1"
    }

    headers = {
        "X-RapidAPI-Key": "YOUR_API_KEY_HERE",
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }

    try:

        response = requests.get(
            url,
            headers=headers,
            params=querystring,
            timeout=30
        )

        data = response.json()

        jobs = []

        for job in data.get("data", []):

            jobs.append({
                "JobTitle": job.get("job_title", ""),
                "Company": job.get("employer_name", ""),
                "Location": job.get("job_city", ""),
                "Skills": "",
                "JobLink": job.get("job_apply_link", ""),
                "Source": "JSearch"
            })

        return pd.DataFrame(jobs)

    except Exception as e:

        print("JSearch Error:", e)

        return pd.DataFrame()