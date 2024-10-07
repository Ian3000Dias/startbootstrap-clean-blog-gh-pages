import smtplib

from flask import Flask, render_template, request
import requests

app = Flask(import_name=__name__)
response = requests.get(url='https://api.npoint.io/722f9e4fa993e2e58985')
response.raise_for_status()

OWN_EMAIL = 'iandias347@gmail.com'
OWN_PASSWORD = 'vmxvvihifaxdbjqv'
print(response.json())

@app.route('/')
def home():
    return render_template('index.html', blog_preview_data = response.json())


@app.route('/about')
def about():
    return render_template('about.html')


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        data = request.form
        name = data["Username"]
        email = data["Email"]
        phone = data["Number"]
        message = data["Message"]
        send_email(name, email, phone, message)
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)

def send_email(name, email, phone, message):
    email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage:{message}"
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(OWN_EMAIL, OWN_PASSWORD)
        connection.sendmail(OWN_EMAIL, OWN_EMAIL, email_message)


# @app.route('/form-entry', methods=['POST'])
# def receive_data():
#     name = request.form['Username']
#     email = request.form['Email']
#     number = request.form['Number']
#     message = request.form['Message']
#     print(f'{name}\n{email}\n{number}\n{message}')
#     return f'<h1>Successfully sent your message</h1>'


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in response.json():
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


if __name__ == '__main__':
    app.run(debug=True)
