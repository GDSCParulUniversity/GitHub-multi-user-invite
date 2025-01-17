import json, requests
from requests.exceptions import RequestException, Timeout
from typing import Optional

class GithubAPIError(Exception):
    """Custom exception for GitHub API errors"""
    def __init__(self, message: str, status_code: Optional[int] = None, response: Optional[dict] = None):
        self.status_code = status_code
        self.response = response
        super().__init__(message)

class github:
    def __init__(self, auth, org=None):
        self.auth = auth
        self.org = org
        self.timeout = 30  # Default timeout in seconds
    
    def gh_request(self, path: str, method="GET", data: dict = {}) -> requests.Response:
        """Make a request to the GitHub API with proper error handling and timeout.

        Args:
            path (str): The API endpoint path
            method (str, optional): HTTP method. Defaults to "GET".
            data (dict, optional): Request payload. Defaults to {}.

        Returns:
            requests.Response: The response from the GitHub API

        Raises:
            GithubAPIError: For GitHub API specific errors
            RequestException: For any request-related errors
            Timeout: For timeout errors
        """
        data = json.dumps(data) if data != {} else None
        
        try:
            res = requests.request(
                method=method, 
                url=f"https://api.github.com{path}", 
                headers={
                    "Accept": "application/vnd.github+json",
                    "Authorization": f"Bearer {self.auth}",
                    "X-GitHub-Api-Version": "2022-11-28"
                }, 
                data=data,
                timeout=self.timeout
            )
            
            if res.status_code == 401:
                raise GithubAPIError("Authentication failed. Please check your GitHub token", res.status_code, res.json())
            elif res.status_code == 403:
                raise GithubAPIError("Rate limit exceeded or insufficient permissions", res.status_code, res.json())
            elif res.status_code >= 500:
                raise GithubAPIError("GitHub server error", res.status_code, res.json())
            
            return res
            
        except Timeout:
            raise GithubAPIError(f"Request timed out after {self.timeout} seconds")
        except RequestException as e:
            if hasattr(e.response, 'status_code'):
                if e.response.status_code == 404:
                    return e.response  # Return 404 response for user checks
            raise GithubAPIError(f"Network error: {str(e)}", getattr(e.response, 'status_code', None))
    
    def invite_user_org(
        self, 
        org: str, user: int, 
        teams: list = [], role: str = "direct_member"
    ) -> requests.Response:
        """
        Invite a user to an organization with the specified role and teams.

        Args:
            org (str): The name of the organization to invite the user to.
            user (int): The ID of the user to invite.
            teams (list, optional): A list of team IDs to add the user to. Defaults to [].
            role (str, optional): The role to assign to the user. Defaults to "direct_member".

        Returns:
            requests.Response: The response object from the GitHub API.
        """
        res = self.gh_request(
            f"/orgs/{org}/invitations",
            method="POST",
            data={
                "invitee_id": user,
                "role": role,
                "team_ids": teams
            }
        )
        
        return res
    
    def get_user_id(self, user: str) -> int | None:
        """
        Get the user ID of a given GitHub username.

        Args:
            user (str): The GitHub username.

        Returns:
            int | None: The user ID if the user exists, otherwise None.
        """
        
        res = self.gh_request(f"/users/{user}")
        if res.status_code == 200:
            return res.json()['id']
        else:
            return None
    
    def list_teams(self, org: str):
        """
        Lists all the teams in the specified organization.
        
        Args:
        - org (str): The name of the organization.
        
        Returns:
        - None
        """
        res = self.gh_request(f"/orgs/{org}/teams")
        
        if res.status_code == 200:
            for team in len(res):
                print(f"{team.name} | id: {team.id}")
        else:
            print("Something unexpected happened")
    
    def is_user_member_of_org(self, org: str, user_id: int) -> bool:
        """
        Check if a user is a member of a GitHub organization.

        Args:
            org (str): The name of the GitHub organization.
            user_id (int): The ID of the user.

        Returns:
            bool: True if the user is a member, False otherwise.
        """
        res = self.gh_request(f"/orgs/{org}/members/{user_id}")
        return res.status_code == 204  # 204 means the user is a member

