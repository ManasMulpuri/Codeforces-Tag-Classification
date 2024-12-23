import requests
import json
import csv

api_key = "jina_ac29ba80c6734d95a30252c078c5f19a6hPIxeEfCL4pnxRdBcJ4CgFup9pw"
headers = {
    "Authorization": f"Bearer {api_key}",
    "X-Retain-Images": "none",
    "Accept": "application/json"
}

def fetch_problems():
    url = "https://codeforces.com/api/problemset.problems"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'OK':
            return data['result']['problems']  # List of problems
        else:
            print(f"Error: {data['comment']}")
    else:
        print(f"HTTP Error: {response.status_code}")

print("\nFetching problems...")
problems = fetch_problems()
print(f"Total problems fetched: {len(problems)}")
file = open('dataset.csv', mode='a', newline='',encoding='utf-8')
writer = csv.writer(file)
for i in range(len(problems)):
    print(i)
    problem = problems[i]
    # print(problem)
    problem_url = f"https://codeforces.com/problemset/problem/{problem['contestId']}/{problem['index']}"
    problem_id = str(problem['contestId']) + str(problem['index'])
    rating = problem.get('rating')
    tags = problem.get('tags')
    jina_url = f"https://r.jina.ai/{problem_url}"
    response = requests.get(jina_url, headers=headers)
    text = response.text
    content = json.loads(response.content)
    problem_description = content.get('data').get('content') if content and content.get('data') else ""
    tags_str = joined_string = '|'.join(tags)
    row = [problem_id,repr(problem_description),rating,tags_str]
    # print(row)
    # break
    writer.writerow(row)
    # break
