from flask import Flask, render_template, request, send_file
from bs4 import BeautifulSoup

app = Flask(__name__, template_folder='templates')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def upload_file():
    following = request.files['following']
    followers = request.files['followers']
    following.save('following.html')
    followers.save('followers.html')

    file = open("./following.txt", 'w')
    file_following = open('./following.html', 'r')
    html_following = file_following.read()
    soup_following = BeautifulSoup(html_following, features="html.parser")

    # kill all script and style elements
    for script in soup_following(["script", "style"]):
        script.extract()    # rip it out

    # get text
    text_following = soup_following.get_text()
    text_following = text_following[59:]

    arr_following = text_following.split(", ")
    arr_following.pop()

    for index, value in enumerate(arr_following):
        if index == 0:
            arr_following[index] = value[:-6]
        else:
            new = value[9:]
            arr_following[index] = new[:-6]

    arr_following = list(filter(None, arr_following))

    for index, value in enumerate(arr_following):
        if value[0].isupper():
            arr_following[index] = value[1:]
        file.write(arr_following[index]+"\n")

    file = open("./follwers.txt", "w")

    file_followers = open('./followers.html', 'r')

    html_followers = file_followers.read()
    soup_followers = BeautifulSoup(html_followers, features="html.parser")

    # kill all script and style elements
    for script in soup_followers(["script", "style"]):
        script.extract()    # rip it out

    # get text_followers
    text_followers = soup_followers.get_text()
    text_followers = text_followers[20:]

    arr_followers = text_followers.split(", ")
    arr_followers.pop()

    for index, value in enumerate(arr_followers):
        if index == 0:
            arr_followers[index] = value[:-6]
        else:
            new = value[9:]
            arr_followers[index] = new[:-6]

    arr_followers = list(filter(None, arr_followers))

    for index, value in enumerate(arr_followers):
        if value[0].isupper():
            arr_followers[index] = value[1:]
        file.write(arr_followers[index]+"\n")

    file = open("unfollowers.txt", "w")
    result = [item for item in arr_following if item not in arr_followers]
    for i in result:
        file.write(i+"\n")

    file.close()
    return send_file("unfollowers.txt", as_attachment=True)
