import matplotlib.pyplot as plt

from src.trend_analysis import get_category_trends
from src.location_analysis import get_top_locations


# Category Graph
categories = get_category_trends()

plt.figure(figsize=(8,5))
plt.bar(categories.keys(), categories.values())
plt.title("Job Category Trends")
plt.tight_layout()
plt.savefig("category_trends.png")
plt.close()


# Location Graph
locations = dict(get_top_locations().most_common(10))

plt.figure(figsize=(10,5))
plt.bar(
    [str(x) for x in locations.keys()],
    list(locations.values())
)
plt.title("Top Locations")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("top_locations.png")
plt.close()

print("Graphs Generated")