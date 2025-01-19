# pylint: disable=missing-module-docstring
import os
import sys
import argparse
from dotenv import load_dotenv
from rich.progress import track
from rich import print as cprint
from requests.exceptions import RequestException, Timeout
from utils import github, GithubAPIError

gh: github


def multi_invite(org: str, a_users: list):
    """
    Invite multiple users to a GitHub organization.

    Args:
        org (str): The name of the GitHub organization.
        users (list): A list of usernames to invite.

    Returns:
        None
    """
    successful_invites = 0
    failed_invites = 0
    already_members = 0
    
    cprint(f"[magenta]  Inviting {len(a_users)} user/s ..")
    
    for user in track(a_users, description="Inviting users"):
        try:
            uid = gh.get_user_id(user)

            if uid is None:
                cprint(f"[red]: User {user} does not exist")
                failed_invites += 1
                continue

            # Check if user is already a member of the organization
            if gh.is_user_member_of_org(org, uid):
                cprint(f"[yellow]: User {user} is already a member of the organization")
                already_members += 1
                continue

            cprint(f"[green]: Sending invite to {user}")
            inv = gh.invite_user_org(org, uid)

            if inv.status_code == 201:
                cprint(f"[green]: Invite sent successfully to {user}")
                successful_invites += 1
            elif inv.status_code == 422:  # 422 Unprocessable Entity
                error_response = inv.json()
                if any(error['code'] == 'unprocessable' for error in error_response.get('errors', [])):
                    cprint(f"[yellow]: User {user} is already invited")
                    already_members += 1
                else:
                    cprint(f"[red]: Could not invite {user}")
                    cprint(f"[gray]: Error details: {error_response}")
                    failed_invites += 1
            else:
                cprint(f"[red]: Could not invite {user}")
                cprint(f"[gray]: Error details: {inv.json()}")
                failed_invites += 1

        except GithubAPIError as e:
            cprint(f"[red]: GitHub API error while processing {user}: {str(e)}")
            if e.status_code:
                cprint(f"[gray]: Status code: {e.status_code}")
            if e.response:
                cprint(f"[gray]: Response details: {e.response}")
            failed_invites += 1
        except Exception as e:
            cprint(f"[red]: Unexpected error while processing {user}: {str(e)}")
            failed_invites += 1

    # Print summary
    cprint("\n[bold]Invitation Summary:")
    cprint(f"[green]✓ Successfully invited: {successful_invites}")
    cprint(f"[yellow]⚠ Already members/invited: {already_members}")
    cprint(f"[red]✗ Failed invites: {failed_invites}")


if __name__ == "__main__":
    # Load environment variables
    if os.path.exists(".env"):
        load_dotenv(".env")

    # Parse arguments
    parser = argparse.ArgumentParser(
        prog="GitHub Organization Inviter",
        epilog="v0.0.1"
    )
    parser.add_argument("--users_file", dest="users_file",
                        help="invite multiple users", required=True)
    parser.add_argument(
        "--org", dest="org", help="The organization to invite the user to.", required=True)
    args = parser.parse_args()

    auth = os.environ["GITHUB_ACCESS_TOKEN"]
    gh = github(auth)

    if not args.org:
        cprint("[red]: requires org name")
        sys.exit(1)

    users = []
    if args.users_file:
        usr_file = args.users_file
        if os.path.exists(usr_file):
            with open(usr_file, 'r', encoding="utf-8") as f:
                users = f.readlines()
                users = [u.strip() for u in users]

            multi_invite(args.org, a_users=users)
