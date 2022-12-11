# Flow ⚡

## Arch

### Flask server

Our backend flask server is responsible for handling all API calls as well as serving local models (should we extend into this domain).

### Browser plugin

Our frontend server is the chrome extension which on-click parses the active tab's DOM and searches and finds the .mp3 files; those .mp3 files are then translated using AssemblyAI and summarized using Cohere.

Has a popup window. Button click triggers

- Extraction of mp3-file download url
- triggering conversion endpoint from our server
- parsing the response to html and inserting it into the pages DOM

## Launching Backend

```bash
cd backend
python -m flask run # now running on localhost:500
```

## API definition

### POST -- /generateblog

expected body params:

- uri (str): The download link of the mp3 file

expected returned data:

- headings (array[str]): An array with the heading of the paragraphs of the blog article
- summaries (array[str]): An array with the body of the paragraphs of the blog article

This will trigger a transcription of the podcast using Assembly's API. The text is then chunked by speaker. Host texts is transformed to headings using Cohere's API. Guest texts are summarized using Cohere's API as well.

## On the browser

Open

> will take about 10 minutes to run  
> `http://localhost:5000/podcast/?uri=https://d3ctxlq1ktw2nl.cloudfront.net/staging/2022-1-23/ebf1141e-02bb-7752-5e74-3aef1d03bbf9.mp3`

Open

> wil take about 15 minutes to run  
> `http://localhost:5000/generateblog/?uri=https://d3ctxlq1ktw2nl.cloudfront.net/staging/2022-1-23/ebf1141e-02bb-7752-5e74-3aef1d03bbf9.mp3`
