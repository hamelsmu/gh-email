from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_emails', methods=['POST'])
def get_emails():
    username = request.form.get('username')
    
    if username.strip() == 'hamelsmu':
        return '@hamelsmu is the author of this app, so he has the privilege of showing you this message instead :)'
    
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
    
    return '<br>'.join(emails) if emails else 'No emails found'

if __name__ == '__main__':
    app.run(debug=True)