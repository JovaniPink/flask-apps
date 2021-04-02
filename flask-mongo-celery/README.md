# Mission to Mars

> Web-scraping with Celery Task and delivering data in a Flask App.

![Mars](resources/mars.png)

<span>Photo by <a href="https://unsplash.com/@lobosnico?utm_source=unsplash&amp;utm_medium=referral&amp;utm_content=creditCopyText">Nicolas Lobos</a> on <a href="https://unsplash.com/s/photos/mars?utm_source=unsplash&amp;utm_medium=referral&amp;utm_content=creditCopyText">Unsplash</a></span>

## Web Scraping

Web scraping simplifies the process of extracting data from sources where APIs are not available. Scraping speeds up the data gathering process by automating steps and creating easy accessible scrapped data in many formats including CSV, JSON, or raw text.

Basically, web scraping saves you the trouble of manually downloading or copying any data and automates the whole process with programmatic tools.

Web Scraping Tools:

- Chrome Driver
- Splinter
- BeautifulSoup
- Pandas (forms)
- Mongo
- Celery
- Flask
- Bootstrap 4
- jQuery

Web Scraping Tools I'm interested in:

- selenium but still using Chrome Driver
- requests
- regex

### Scrape Mars News

- Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text from https://mars.nasa.gov/news/

### Featured Image

- Heading over to https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars for Featured Image
- Use Splinter and Chrome Driver to navigate the site and find the image URL for the current Featured Mars Image and assign the relative image url string to a variable called img_url_rel

### Mars Facts

- Visit the Mars Facts webpage and use Pandas' read_html method to grab the page's table
- Use Pandas' to_html method to convert the table data to a HTML table with classes

### Mars Hemispheres

- Visit https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars site to scrape high resolution images for each of Mar's hemispheres
- We are saving the hemisphere image, and the Hemisphere title containing the hemisphere name

* Using well organized directories with comments
  - /.vscode # Proper testing and source code editing
  - /notebooks # Holding practice.ipynb, mission_to_mars.ipynb & mission_to_mars_challenge.ipynb
  - /resources # Screenshots that the app works.
  - /static # css, js, fonts, etc
  - /templates # Jinja2 HTML template files with Bootstrap 4
  - .editorconfig # .editorconfig to power some workflows in VS Code.
  - .gitignore # .gitignore
  - app.py # The Module's Flask app but running with celery
  - scraping.py # scrape_all function that decorated with a celery.task function

## Storing Data

We worked on our scraping script within Jupyter Notebook and then exported the code into a Python Script called scraping.py. With a function called scrape_all that decorated with a celery.task function. MongoDB is used for persistence and as a broker for Celery. I really wanted to use Celery for this module seeing that many scripts that we would be running are computational taxing and could be awesome to have a task queue to break up work.

## Serving Data

### Usage

Running this app requires you to have a mongo, celery, and flask server running at the same time.

```powershell
PS ~/mission-to-mars/> mongod
```

```powershell
PS ~/mission-to-mars/> celery -A app.celery worker --pool=solo -l info
```

```powershell
PS ~/mission-to-mars/> $env:FLASK_APP = 'app'
PS ~/mission-to-mars/> $env:FLASK_ENV = 'development'
PS ~/mission-to-mars/> python app.py
```

### Routes

/ # index route
/longtask # jQuery route that starts the Celery Long Task
/status/<task_id> # jQuery route that checks on the status of the task

### Data Powering the Web app

- MongoDB is used for persistence and as a broker for Celery. With Flask and HTML we display all of the information that was scraped from the URLs and stored in Mongo.

## Todo Checklist

A helpful checklist to gauge how your README is coming on what I would like to finish:

- [ ] PYTHON REQUIREMENTS FILE! pipenv?!?
- [ ] Update the UI/UX.
- [ ] jQuery needs work.
- [ ] State management and logic with the Fetch button

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
