from fasthtml.common import *
from httpx import get

app, rt = fast_app()

@rt("/")
def get():
    return Titled("GitHub Email Finder", 
        A("Code on GitHub", href="https://github.com/hamelsmu/gh-email/tree/main/fasthtml"),
        Form(hx_post="/get_emails", hx_target="#results")(
            Label("GitHub Username", Input(name="username")),
            Button("Get Emails", type="submit")
        ),
        Div(id="results")
    )

@rt("/get_emails")
def post(username: str):
    if username.strip() == 'hamelsmu':
        return P("@hamelsmu is the author of this app, so he has the privilege of showing you this message instead :)")
    
    events = get(f"https://api.github.com/users/{username}/events/public", timeout=10).json()    
    emails = set()
    for event in events:
        for commit in event.get('payload', {}).get('commits', []):
            author = commit.get('author', {})
            name, email = author.get('name'), author.get('email')
            if name and email and 'github-action' not in name:
                emails.add(f"{name}: {email}")
    
    if emails:
        return Ul(*[Li(email) for email in emails])
    else:
        return P("No emails found")

serve()