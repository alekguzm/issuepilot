# Gather issues from github repos

import requests
from requests.exceptions import HTTPError
import json
from datetime import datetime, timezone
from pathlib import Path

#Get issues from github repo
#PARAMS: owner, repo, per_page=# of issues on each page, num_pages
#RETURNS: raw list of issues
def get_issues(owner, repo, state, per_page, num_pages):

    url = f"https://api.github.com/search/issues"

    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }

    raw_issues = []
    raw_counter = 0
    
    for page in range(1, num_pages+1):

        query_params = {
            "q": f"repo:{owner}/{repo} type:issue ",
            "per_page": per_page,
            "page": page
        }
        if state == 'open':
            query_params["q"] += "is:open"
        elif state == 'closed':
            query_params["q"] += "is:closed"

        try:
            r = requests.get(url, 
                params=query_params, 
                headers=headers,
                timeout=15.0)

            r.raise_for_status()

            converted_page = r.json()["items"]
            raw_counter += len(converted_page)

            raw_issues += converted_page

            if len(converted_page) < per_page:
                break

        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            return None
        except requests.exceptions.Timeout:
            print("The request timed out.")
            return None
        except requests.exceptions.RequestException as e:
            print(f"An error has occurred: {e}")
            return None

    print(f"Raw API results inspected: {raw_counter}")

    return raw_issues

#Simplify each issue (keep only important features)
#PARAMS: issues, owner, repo
#RETURNS: cleaner list of issues
def normalize_issues(issues, owner, repo):

    new_issues = []

    collected_at_time = datetime.now(timezone.utc).isoformat()

    for issue in issues:
        temp_dict = {}
        temp_dict["repository"] = f"{owner}/{repo}"
        temp_dict["issue_number"] = issue["number"]
        temp_dict["title"] = issue["title"]
        temp_dict["body"] = issue["body"]

        labels = issue['labels']
        temp_dict['labels'] = [item['name'] for item in labels]

        temp_dict["state"] = issue["state"]
        temp_dict["created_at"] = issue["created_at"]
        temp_dict["updated_at"] = issue["updated_at"]
        temp_dict["closed_at"] = issue["closed_at"]
        temp_dict["comments_count"] = issue["comments"]
        temp_dict["html_url"] = issue["html_url"]

        temp_dict["collected_at"] = collected_at_time

        new_issues.append(temp_dict)

    return new_issues

#Combine get_issues, and normalize_issues
#This will get the issues from the repo, filter out the pulls, and fix the dictionary
def full_retrieve(owner, repo, state="all", per_page=30, num_pages=1): #default (Dont touch)

    raw_issues = get_issues(owner, repo, state, per_page, num_pages)
    if raw_issues is None:
        return None
    
    all_set_issues = normalize_issues(raw_issues, owner, repo)
    return all_set_issues

#Used when im gathing data for training
#not used by user
if __name__ == "__main__":

    scikit_owner = "scikit-learn"
    scikit_repo = "scikit-learn"
    pandas_owner = "pandas-dev"
    pandas_repo = "pandas"
    vue_owner = "vuejs"
    vue_repo = "vue"

    owner = pandas_owner
    repo = pandas_repo

    all_set_issues = full_retrieve(owner, repo, per_page=100, num_pages=3)

    root_path = Path(__file__).resolve().parents[2]
    filename = root_path / "data" / "raw" / f"{owner}_{repo}.json"

    filename.parent.mkdir(parents=True, exist_ok=True)

    if all_set_issues is not None:
        with open (filename, 'w', encoding='utf-8') as f:
            json.dump(all_set_issues, f, indent=4, ensure_ascii=False)
