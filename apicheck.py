from serpapi import GoogleSearch

params = {
  "engine": "google",
  "q": "Coffee",
  "api_key": "bff8867afab52fb1426a7ecaacebeb2eaf826b9cd7e2edf872a96865eec8f416"
}

search = GoogleSearch(params)
results = search.get_dict()
organic_results = results["organic_results"]

for result in organic_results:
    title = result["title"]
    link = result["link"]
    print(f"{title}: {link}")

print(organic_results)