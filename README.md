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
> You should have owner/admin access to the organization.

Edit file 'users.txt' with the list of users to invite. There should only be one user per line.

Example of 'users.txt' file:

```txt
saicharankandukuri
vinci-d
torvalds
```

> **Warning**
> Cross check the usernames before adding them to the list for safety of the organization.

Run the script:

```bash
python3 main.py --org your_org_name --users_file users.txt
```

## Contributing

1. Fork the repository
2. Clone your fork
```bash
git clone https://github.com/<your-username-here>/Github-multi-user-invite.git
```
3. Navigate to the project directory
```bash
cd github-multi-user-invite
```
4. Install dependencies
```bash
pip install -r requirements.txt
```
5. Make changes that you want
6. Submit pull request

All pull requests are welcome. 
For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License.
