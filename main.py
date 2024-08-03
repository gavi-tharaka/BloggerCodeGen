from flask import Flask, render_template_string, request
import imdb
import random
from pyngrok import ngrok
app = Flask(__name__)


html_code = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Download Page</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
            background-color: #f4f4f4;
        }

        .banner {
            width: 100%;
            max-width: 800px;
            height: 300px;
            overflow: hidden;
            margin-bottom: 20px;
        }

        .banner img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }

        .content {
            text-align: center;
        }

        .download-button {
            padding: 15px 25px;
            font-size: 18px;
            color: white;
            background-color: #007bff;
            border: none;
            border-radius: 5px;
            cursor: not-allowed;
            text-decoration: none;
            pointer-events: none;
        }

        .download-button.enabled {
            cursor: pointer;
            pointer-events: auto;
            background-color: #007bff;
        }

        .download-button.enabled:hover {
            background-color: #0056b3;
        }

        .countdown {
            margin-top: 20px;
            font-size: 16px;
            color: #333;
        }
    </style>
</head>
<body>

    <div class="banner">
        <img src="{{poster}}" alt="Banner Image">
    </div>
    <p>{{description}}</p>
    <div class="content">
        <a href="{{redirectURL}}" download class="download-button" id="download-button">Download Full Movie</a>
        <div class="countdown">Wait <span id="countdown">5</span> seconds...</div>
    </div>

    <script>
        let countdownElement = document.getElementById('countdown');
        let downloadButton = document.getElementById('download-button');
        let countdown = 5;

        const countdownInterval = setInterval(() => {
            countdown--;
            countdownElement.textContent = countdown;

            if (countdown >= 0) {
                clearInterval(countdownInterval);
                downloadButton.classList.add('enabled');
                downloadButton.style.cursor = 'pointer';
                downloadButton.style.pointerEvents = 'auto';
                setTimeout(() => {
                    window.location.href = "{{redirectURL}}";
                }, 1000); // Additional 1 second delay for UX clarity
            }
        }, 1000);
    </script>

</body>
</html>

'''

template = """
<head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Download Page</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #f4f4f4;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background: #fff;
                border-radius: 8px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
            h1 {
                text-align: center;
            }
            .form-group {
                margin-bottom: 15px;
            }
            label {
                display: block;
                margin-bottom: 5px;
            }
            input[type="text"] {
                width: calc(100% - 22px);
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            button {
                background-color: #007bff;
                color: #fff;
                border: none;
                padding: 10px 20px;
                border-radius: 4px;
                cursor: pointer;
                font-size: 16px;
            }
            button:hover {
                background-color: #0056b3;
            }
            textarea {
                width: 100%;
                height: 150px;
                margin-top: 20px;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-family: monospace;
                background: #f9f9f9;
                resize: none;
            }
            .code-container {
                margin-top: 20px;
            }
            .code-container pre {
                white-space: pre-wrap;
            }
        </style>
    </head>
<!-- HTML form to input download link and image link -->
<body>
        <div class="container">
            <h1>Generate Download Page HTML</h1>
            <form method="get" action="">
                <div class="form-group">
                    <label for="downloadLink">Movie Name :  </label>
                    <input type="text" id="downloadLink" name="name" required value="{{title}}">
                </div>
                <button type="submit">Generate HTML</button>
            </form>
            <textarea id="code" rows="10" cols="50">{{html_code}}</textarea>
            <button onclick="copyToClipboard()">Copy to Clipboard</button>
        </div>
    <script>
    function copyToClipboard() {
        var code = document.getElementById("code");
        code.select();
        document.execCommand("copy");
        alert("HTML code copied to clipboard!");
    }
    </script>
</body>
"""


@app.route('/')
def index():
    # Initialize the IMDb object
    movie_name = request.args.get('name', default="the 100")
    ia = imdb.IMDb()
    mId = ia.search_movie(movie_name)[0].movieID
    movie = ia.get_movie(mId)
    year = movie['year']
    title = movie.get('title')

    if year:
        title = title + f' ({year})'
    description = movie.get('plot outline')
    banner = movie.get_fullsizeURL()
    print(title)
    html_Code = html_code.replace("{{poster}}", banner).replace("{{description}}", description).replace("{{redirectURL}}", random.choice(open("rederect.txt", 'r').readlines()))
    return render_template_string(template, html_code=html_Code, title=title)


if __name__ == '__main__':
    ngrok.set_auth_token("2k7XmxwTv7XmK9QLN6zCUXIHRGU_3gKNZYQkdQpJuzjX5uX5M")
    ngrok_tunnel = ngrok.connect(5000)
    print('Public URL:', ngrok_tunnel.public_url)
    app.run()
