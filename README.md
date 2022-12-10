<<<<<<< HEAD
# flow
=======
# flow

## Arch

### Browser plugin
Has a popup window. Button click triggers 
- extraction of mp3-file download url
- triggering conversion endpoint from our server
- parsing the response to html and inserting it into the pages DOM

### API definition
#### POST -- /generateblog
expected body params: 
- audio_url (str): The download link of the mp3 file

expected returned data:
- headings (array[str]): An array with the heading of the paragraphs of the blog article
- paragraphs (array[str]): An array with the body of the paragraphs of the blog article

## API keys

### Assembly AI 
Key: 3d7fa80c0b1748eaaa5df94b65729cb4

### Uberduck
Creator plan

Key:  pub_eodanjxhqigxveqxpo
Secret: pk_424eedb6-c803-4f25-9116-8b054354e9fb

### Cohere
Key: Pp0haiyiyMTfS4VHPCacV3W27tGF8tK7Bzmoz0dZ 
>>>>>>> 1a06f41 (Add extension stub)
