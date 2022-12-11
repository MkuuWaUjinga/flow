const button = document.querySelector("button");
button.addEventListener("click", async () => {
    console.log(`Flow triggered`);
    chrome.tabs.query({ active: true, currentWindow: true }, function (tab) {
        chrome.tabs.sendMessage(tab[0].id, {msg: "flow-click"});
    })
});
