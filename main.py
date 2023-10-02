# pylint: disable=missing-module-docstring
import os
import sys
import argparse
from dotenv import load_dotenv
from rich.progress import track
from rich.console import Console
from rich import print as cprint
from utils import github

gh: github
console = Console()


def multi_invite(org: str, users_file: str):
    """
    Invite multiple users to a GitHub organization with specified roles.

    Args:
        org (str): The name of the GitHub organization.
        users_file (str): Path to the file containing usernames and roles.

    Returns:
        None
    """
    # Load users and roles
    users_with_roles = []
    valid_roles = ["admin", "direct_member", "billing_manager"]

    if os.path.exists(users_file):
        with open(users_file, 'r', encoding="utf-8") as f:
            users_with_roles = f.readlines()
            users_with_roles = [line.strip().split(':') for line in users_with_roles]

    # Invite users with roles
    cprint(f"[magenta]  Inviting {len(users_with_roles)} user/s ..")

    for idx, user_role_tuple in track(enumerate(users_with_roles), total=len(users_with_roles), description="Inviting users"):
        if len(user_role_tuple) != 2:
            cprint(f"[yellow]: Invalid format in line {idx + 1}. Skipping.")
            continue

        user, role = map(str.strip, user_role_tuple)

        if role not in valid_roles:
            cprint(f"[yellow]: Invalid role {role} specified for user {user}. Skipping.")
            continue

        uid = gh.get_user_id(user)

        if uid is None:
            cprint(f"[red]: user {user} does not exist")
            continue

        # Check if user is already a member of the organization
        if gh.is_user_member_of_org(org, uid):
            cprint(f"[yellow]: user {user} is already a member of the organization")
            continue

        cprint(f"[green]: sending invite to {user} with role {role}.")
        inv = gh.invite_user_org(org, uid, role=role)

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
                        help="invite multiple users with roles", required=True)
    parser.add_argument(
        "--org", dest="org", help="The organization to invite the user to.", required=True)
    args = parser.parse_args()

    auth = os.environ["GITHUB_ACCESS_TOKEN"]
    gh = github(auth)

    if not args.org:
        cprint("[red]: requires org name")
        sys.exit(1)

    if args.users_file:
        multi_invite(args.org, users_file=args.users_file)
