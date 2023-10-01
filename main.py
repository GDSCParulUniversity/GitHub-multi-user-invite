# pylint: disable=missing-module-docstring
import os
import sys
import argparse
from dotenv import load_dotenv
from rich.progress import track
from rich import print as cprint
from utils import github

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
    # check if user exists
    cprint(f"[magenta]  Inviting {len(a_users)} user/s ..")
    for user in track(a_users, description="Inviting users"):
        uid = gh.get_user_id(user)

        if uid is None:
            cprint(f"[red]: user {user} does not exist")
            continue

        # Check if user is already a member of the organization
        if gh.is_user_member_of_org(org, uid):
            cprint(f"[yellow]: user {user} is already a member of the organization")
            continue

        cprint(f"[green]: sending invite to {user}.")
        inv = gh.invite_user_org(org, uid)

        if inv.status_code == 201:
            cprint(f"[green]: invite sent to {user}.")
        elif inv.status_code == 422:  # 422 Unprocessable Entity
            error_response = inv.json()
            if any(error['code'] == 'unprocessable' for error in error_response.get('errors', [])):
                cprint(f"[yellow]: user {user} is already invited")
            else:
                print(f"[red]: couldn't invite {user}")
                print(f"[gray]: LOG: {error_response}")
        else:
            print(f"[red]: couldn't invite {user}")
            print(f"[gray]: LOG: {inv.json()}")


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
