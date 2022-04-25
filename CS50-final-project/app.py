from flask import Flask, redirect, render_template, request
import os

import googleapiclient.discovery

app = Flask(__name__)


# Retrieve videos from youtube
def playlist(yearStart, yearEnd, genre):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = os.environ.get("API_KEY")

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

    request = youtube.search().list(
        part="snippet, id",
        maxResults=3,
        order="viewCount",
        publishedAfter=f"{yearStart}-01-01T00:00:00Z",
        publishedBefore=f"{yearEnd}-01-01T00:00:00Z",
        topicId=f"{genre}",
        type="video",
        videoCategoryId="10",
        videoEmbeddable="true"
    )
    response = request.execute()
    
    # Store id of retrieved videos in a list
    videoId = []
    for i in range(3):
        videoId.append(response["items"][i]["id"]["videoId"])
    
    # Store list of video names
    videoName = []
    for i in range(3):
        videoName.append(response["items"][i]["snippet"]["title"])

    output = [videoId, videoName]
    
    return output

   
@app.route("/")
def index():
        return render_template("index.html")


# Results page with retrieved videos
@app.route("/results", methods=["POST"])
def results():
    # Store user input in variables
    yearStart = request.form.get("years", type=int)
    print(yearStart)
    yearEnd = yearStart + 1
    genre = request.form.get("genres")

    # Call function to retrieve videos from youtube
    output = playlist(yearStart, yearEnd, genre)
    
    genreDict = {
        "/m/04rlf": "Music",
        "/m/05fw6t": "Children's music",
        "/m/02mscn": "Christian music",
        "/m/0ggq0m": "Classical music",
        "/m/01lyv": "Country",
        "/m/02lkt": "Electronic music",
        "/m/0glt670": "Hip hop music",
        "/m/05rwpb": "Independent music",
        "/m/03_d0": "Jazz",
        "/m/028sqc": "Music of Asia",
        "/m/0g293": "Music of Latin America",
        "/m/064t9": "Pop music",
        "/m/06cqb": "Reggae",
        "/m/06j6l": "Rhythm and blues",
        "/m/06by7": "Rock music",
        "/m/0gywn": "Soul music"
    }

    # Deal with different genres in header (result page)
    genreInHeader = genreDict[genre]

    return render_template("results.html", year=yearStart, output=output, genre=genreInHeader)