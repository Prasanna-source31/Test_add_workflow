import os
import requests

def copy_file_to_repo(repo_name, token):
    url = f'https://api.github.com/repos/ORG_NAME/{repo_name}/contents/.github/workflows/terrascan.yml'
    headers = {'Authorization': f'Bearer {token}'}
    
    with open('.github/workflows/terrascan.yml', 'r') as file:
        content = file.read()

    data = {
        'message': 'Copy terrascan.yml',
        'content': content,
    }

    response = requests.put(url, json=data, headers=headers)
    if response.status_code == 201:
        print(f'terrascan.yml copied to {repo_name}')
    else:
        print(f'Error copying terrascan.yml to {repo_name}: {response.text}')

def main():
    org_name = 'Prasanna-source31'
    token = os.environ[${{ secrets.TEST_TOKEN }}]  # GitHub Personal Access Token

    response = requests.get(f'https://api.github.com/orgs/{org_name}/repos', headers={'Authorization': f'Bearer {token}'})
    repos = response.json()

    for repo in repos:
        copy_file_to_repo(repo['name'], token)

if __name__ == '__main__':
    main()
