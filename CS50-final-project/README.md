# YouTube hitparade
#### Video Demo:  <https://youtu.be/4FV58w5JizU>
#### Description:
My CS50 final project is a web application wirtten in Python, using Flask framework. The purpose of this application is to display the 3 most viewed music videos in given genre, that were published in a particular year.

This app can be useful for someone who is interested in the history of music videos published on YouTube or just wants to watch the most popular music videos in their favorite genre for fun.

The application consists of the following files:

### app.py

Main file containing function that retrieves the data from YouTube. This is executed via youtube v3 API, Search: list method in particular, and only the videos that match user's input are retrieved. First,  googleapiclient.discovery is imported. Then the *playlist* function is defined. The inputs into this function are the three variables that are used in request in order to get response from youtube API. After receiving response from API, the video IDs and video titles are stored in a variable and this is the output of the *playlist* function. Then there are *index* function and *results* functions, which render templates. *index* function renders the home page with a form and a short description. *results* function first stores user input into variables, then calls *playlist* function with these variables as inputs and renders template with the results.

### html pages

There are two html pages. On the first page index.html, there is a basic description of the app and a form, where the user enters desired year and genre. Clicking the submit button will render results.html page containing embedded videos and song titles. Jinja variables are used to automatically display correct song titles. To insert the correct *src* attribute to the *iframe* element, there is a hidden *p* element, that contains link to the video. This link is inserted into the *iframe* by using javascript.

### styles.css

Style of html pages was created with user friendliness in mind. The user only needs three clicks to select and view the desired videos. The form was designed as dominant feature on the index.html page. Responsive design was made using media query.

### Application settings

For the application to work properly, developer must set the API key, which they obtain on [Google Cloud Platform](https://console.cloud.google.com/) in the Credentials section.  This API then will be stored as an environment variable using the  `export API_KEY=yourKey` command. The Google APIs Client Library for Python and libraries for user authorization must be installed as well, if they have not been installed before:
`pip install --upgrade google-api-python-client` and `pip install --upgrade google-auth-oauthlib google-auth-httplib2`.

### Technologies used

- Python
- Flask
- Javascript
- HTML
- CSS
- Jinja2


