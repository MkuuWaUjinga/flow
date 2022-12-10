// Current status:
// There are two script types: content script and action script
// the action script is executed within the plugin and has no access to the DOM of the webpage. it console logs to the plugin as well.
// the content script has only access to the webpage. it console logs to the webpage.
// this script serves as both: a content and and action script.
// https://stackoverflow.com/questions/69714540/chrome-extension-command-passing-to-content-script (this should fix it)
// @adrian will fix later
const mp3url = document.querySelector('audio').firstChild.getAttribute('src');
console.log(mp3url);

const button = document.querySelector("button");
button.addEventListener("click", async () => {
  // Get podcast download URL from DOM
  console.log("hi");
  console.log(mp3url);
  let headings;
  let bodies;
  if (mp3url) {
    // Convert podcast to text using assembly's API. We coudla lso already use the API to get a summary of the transcript -- Assembly supports that
    // Convert summarized text to blog article using Cohere's API
    // ideas: we might have to chunk the transcript into different parts -> for each part we'd generate a heading and a text body using cohere's api.
    // Load text into DOM
    console.log(mp3url)
    headings = []
    bodies = ["joooo", "this is a littttt blog post", "guess what", "it's AI-generated"]
    const insertPoint = document.querySelector('p');
    for (let body in bodies) {
      const paragraph = document.createElement('p');
      paragraph.textContent = body;
      insertPoint.insertAdjacentElement("beforebegin", paragraph);
    }

  }
});
