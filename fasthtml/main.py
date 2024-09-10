from fasthtml.common import *
import httpx

bttn_style = StyleX('assets/button.css')
copyfn = ScriptX('assets/copy.js')
fa = Link(rel="stylesheet", href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.6.0/css/all.min.css")

app, rt = fast_app(hdrs=(fa, bttn_style, copyfn))

@rt("/")
def get():
    return (
        Title("GitHub Email Finder"), 
        Main(
            Grid(H1("GitHub Email Finder"),
                Div(A("See Code on", I(cls="fab fa-github"), href="https://github.com/hamelsmu/gh-email/tree/main/fasthtml"), style="text-align: right;")),
            Form(hx_post="/get_emails", hx_target="#results")(
                Input(name="username", placeholder="Enter a GitHub username"),
                Button("Get Emails", type="submit")),
            Div(id="results"),
       cls="container")
    )

@rt("/get_emails")
def post(username: str):
    if username.strip() == 'hamelsmu':
        return P("@hamelsmu is the author of this app, so he has the privilege of showing you this message instead :)")
    
    events = httpx.get(f"https://api.github.com/users/{username}/events/public", timeout=10).json()   
    emails = set()
    for event in events:
        for commit in event.get('payload', {}).get('commits', []):
            author = commit.get('author', {})
            name, email = author.get('name'), author.get('email')
            if name and email and 'github-action' not in name:
                emails.add(f"{name}: {email}")
    
    if emails:
        return Div(
            H2("Results"),
            Table(Tr(Th("Name"), Th("Email")),
                *[Tr(Td(name), Td(Code(email, cls="email-text"),
                            Button(I(cls="fas fa-copy"),
                                Span("Copy", cls="button-text"),
                                cls="copy-btn",
                                hx_on_click=f"copyToClipboard(event, '{email}')"
                            )
                        )
                    ) for name, email in (email.split(": ", 1) for email in emails)
                ]
            )
        )
    else:
        return P("No emails found")

serve()