from fasthtml.common import *
import requests

app, rt = fast_app()

@rt("/")
def get():
    return Titled("GitHub Email Finder", 
        Form(method="post", action="/get_emails")(
            Label("GitHub Username", Input(name="username")),
            Button("Get Emails", type="submit")
        )
    )

@rt("/get_emails")
def post(username: str):
    if username.strip() == 'hamelsmu':
        return Titled("Special Message", 
            P("@hamelsmu is the author of this app, so he has the privilege of showing you this message instead :)")
        )
    
    emails = set()
    response = requests.get(f"https://api.github.com/users/{username}/events/public")
    events = response.json()
    
    for event in events:
        commits = event.get('payload', {}).get('commits', [])
        for commit in commits:
            author = commit.get('author', {})
            name = author.get('name', '')
            email = author.get('email', '')
            if name and email and 'github-action' not in name:
                emails.add(f"{name}: {email}")
    
    if emails:
        return Titled("Email Results", 
            Ul(*[Li(email) for email in emails])
        )
    else:
        return Titled("No Results", P("No emails found"))

serve()