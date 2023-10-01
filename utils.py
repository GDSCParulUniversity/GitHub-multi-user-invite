import json, requests
class github:
    def __init__(self, auth, org=None):
        self.auth = auth
        self.org = org
    
    def gh_request(self, path: str, method="GET", data: dict = {}) -> requests.Response:
        """Make a request to the GitHub API.
        """
        data = json.dumps(data) if data != {} else None
        
        res = requests.request(
            method=method, url=f"https://api.github.com{path}", 
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {self.auth}",
                "X-GitHub-Api-Version": "2022-11-28"
            }, 
            data=data
        )
        
        return res
    
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

