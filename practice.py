import requests

response = requests.get("https://api.github.com/users/octocat")

if response.status_code == 200:
    data = response.json()
    print(data['name'],data['company'],data['location'],data['type'],data['public_repos'])