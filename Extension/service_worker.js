const backendURL = 'http://localhost:8000/check';
var sessionID = ''
chrome.webNavigation.onBeforeNavigate.addListener((details) => {
    if (sessionID == '') {
        console.log('Did not log in!')
        return
    }
    var { tabId, url } = details;
    const urlObj = new URL(url)
    url = urlObj.protocol + '//' + urlObj.hostname + '/';
    // Send a request to the backend to check if the website should be blocked
    fetch(backendURL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            link: url,
            sessionID: sessionID
        })
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not OK');
            }
            return response.json();
        })
        .then(data => {
            console.log(data)
            if (data.block) {
                let cause = data['why'] || 'Blocked by admin';
                let redirectURL = chrome.runtime.getURL(`blocked.html?data=${encodeURIComponent(url)}&cause=${encodeURIComponent(cause)}`);
                chrome.tabs.update(tabId, { url: redirectURL });
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}, { url: [{ schemes: ['http', 'https'] }] });

chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
    if (request.action === "openTechDetailsTab") {
        const data = encodeURIComponent(JSON.stringify(request.data));
        const newTabUrl = chrome.runtime.getURL(`technical_details.html?data=${data}`);
        chrome.tabs.create({ url: newTabUrl });
    }

    if (request.action === 'setSessionKey') {
        console.log(request.sessionKey + 'SW')
        sessionID = request.sessionKey
        chrome.storage.local.set({ sessionKey: request.sessionKey });
    }
});


