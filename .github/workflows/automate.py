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
    token = os.environ.get("GITHUB_TOKEN")  # GitHub Personal Access Token

    response = requests.get(f'https://api.github.com/orgs/{org_name}/repos', headers={'Authorization': f'Bearer {token}'})
    repos = response.json()

    for repo in repos:
        copy_file_to_repo(repo['name'], token)

if __name__ == '__main__':
    main()
- name: Send Teams Notification
  if: ${{ always() }}
  env:
    TEAMS_WEBHOOK_URL: ${{ secrets.TEAMS_WEBHOOK_URL }}
  run: |
    if [[ "${{ job.status }}" == "success" ]]; then
      status_text="succeeded"
      status_color="#36a64f"
    fi

    if [[ "${{ job.status }}" == "failure" ]]; then
      status_text="failed"
      status_color="#d9534f"
    fi

    project_key="${{ steps.get_project_key.outputs.project_key }}"
    report_url="http://20.113.139.49:9000/dashboard?id=$project_key"
    echo "Report URL: $report_url"
    workflow_file_name="${GITHUB_WORKFLOW}"
    workflow_file_url="${GITHUB_SERVER_URL}/${GITHUB_REPOSITORY}/actions/runs/${GITHUB_RUN_ID}?check_suite_focus=true"
    payload="{
      \"@type\": \"MessageCard\",
      \"themeColor\": \"${status_color}\",
      \"title\": \"GitHub Actions Workflow\",
      \"text\": \"Workflow has ${status_text}: ${{ github.repository }}\",
      \"sections\": [
        {
          \"activityTitle\": \"SonarQube Analysis\",
          \"activitySubtitle\": \"${status_text}\",
          \"activityImage\": \"https://www.sonarqube.org/logos/index/favicon.png\",
          \"facts\": [
            {
              \"name\": \"Repository\",
              \"value\": \"${{ github.repository }}\"
            },
            {
              \"name\": \"Report\",
              \"value\": \"[SonarQube Analysis Report](${report_url})\"
            },
            {
              \"name\": \"Workflow File\",
              \"value\": \"[${workflow_file_name}](${workflow_file_url})\"
            }
          ]
        }
      ]
    }"

    curl -X POST -H "Content-Type: application/json" -d "$payload" $TEAMS_WEBHOOK_URL
