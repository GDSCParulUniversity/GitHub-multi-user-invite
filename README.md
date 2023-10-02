
<div align="center">
  <h1>GitHub Multi User Invite 🚀</h1>
  <p>A simple script to invite multiple users to a GitHub organization.</p>
</div>

## How To Use :

1. **Clone this repository & install dependencies:** 

   ```bash
   git clone https://github.com/GDSCParulUniversity/Github-multi-user-invite.git
   cd github-multi-user-invite
   pip install -r requirements.txt` 

2.  **Create a personal access token:**
    
    Create a personal access token with the `admin:org` scope from GitHub and create a `.env` file with the following content:
    
    makefileCopy code
    
    `GITHUB_ACCESS_TOKEN=your_token_here` 
    
    

> **Note:**
> You should be have owner/admin access to the organization.
> You should have owner/admin access to the organization.

    
3.  **Prepare a list of users:**
    
    Create a file (e.g., `users.txt`) with the list of users to invite, one per line.
    
    Example:
    
    Copy code
    
    `saicharankandukuri:admin`
    
    `vinci-d:direct-member`
    
    `torvalds:billing-member` 
    
   > *Warning:*
   > Cross check the usernames before adding them to the list for safety.
   > Cross check the usernames before adding them to the list for safety of the organization.
    
5.  **Run the script:**
    
    bashCopy code
    
    `python3 main.py --org your_org_name --users_file users.txt` 
    

## Contributing 🤝

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License 📝

This project is licensed under the MIT License.
