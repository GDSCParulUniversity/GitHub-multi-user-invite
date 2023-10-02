# GitHub Multi user invite

A simple script to invite multiple users to a GitHub organization.

## Usage

Clone this repository & install dependencies:

```bash
git clone https://github.com/GDSCParulUniversity/Github-multi-user-invite.git
cd github-multi-user-invite
pip install -r requirements.txt
```

Create a personal access token with the `admin:org` scope from [GitHub](https://github.com/settings/tokens) and create a `.env` file with the following content:

```bash
GITHUB_ACCESS_TOKEN=your_token_here
```

> **Note**
> You should be have owner/admin access to the organization.

Create a file ( e.g. `users.txt` ) with the list of users to invite, one per line. You can include a role by including `username:role` with options being `admin`, `direct_member` or `billing_manager`, otherwise roles will default to `direct_member`.

example:

```txt
saicharankandukuri
vinci-d:admin
torvalds
```

> **Warning**
> Cross check the usernames and roles (if any) before adding them to the list for safety.

Run the script:

```bash
python3 main.py --org your_org_name --users_file users.txt
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License.
