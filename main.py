from src.skill_extraction import get_top_skills
from src.location_analysis import get_top_locations
from src.job_classification import classify_jobs
from src.trend_analysis import get_category_trends

# Top Skills
skill_count = get_top_skills()

print("Top Skills:\n")

for skill, count in skill_count.most_common(5):
    print(f"{skill}: {count}")

# Top Locations
location_count = get_top_locations()

print("\nTop Locations:\n")

for location, count in location_count.items():
    print(f"{location}: {count}")

# Job Classification
print("\nJob Classification:\n")

classified_jobs = classify_jobs()

print(classified_jobs)
print("\nCategory Trends:\n")

category_count = get_category_trends()

for category, count in category_count.items():
    print(f"{category}: {count}")