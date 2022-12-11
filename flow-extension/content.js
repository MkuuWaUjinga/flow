if (!window.firstTimeExecuted) {
    window.firstTimeExecuted = true;
    chrome.runtime.onMessage.addListener((data, sender, sendResponse) => {
        if (data.msg == 'flow-click') {
            const mp3url = document.querySelector('audio').firstChild.getAttribute('src');
            console.log(mp3url);
            if (mp3url) {
                // Convert podcast to text using assembly's API. We coudla lso already use the API to get a summary of the transcript -- Assembly supports that
                // Convert summarized text to blog article using Cohere's API
                // ideas: we might have to chunk the transcript into different parts -> for each part we'd generate a heading and a text body using cohere's api.
                // Load text into DOM
                const endpoint_url = "http://localhost:5000/generateblog?uri=" + mp3url
                fetch(endpoint_url).then(response => response.text()).then(data =>
                    {
                        const parsed_data = JSON.parse(data)
                        console.log(parsed_data)
                        const headings = parsed_data.headlines
                        const bodies = parsed_data.summaries
                        let zipped = headings.map(function(e, i) {
                            return [e, bodies[i]];
                        });
                        console.log(zipped)
                        const insertPoint = document.querySelector('p');
                        for (const headingAndBody of zipped) {
                            let heading = headingAndBody[0]
                            let body = headingAndBody[1]
                            const headlineElement = document.createElement('h2');
                            const paragraphElement = document.createElement('p');
                            headlineElement.textContent = heading;
                            paragraphElement.textContent = body;
                            insertPoint.insertAdjacentElement("beforebegin", headlineElement);
                            insertPoint.insertAdjacentElement("beforebegin", paragraphElement);
                        }
                    }
                )
            }
        }
    });
}
