const backendURL = 'http://localhost:8000/check';

chrome.webNavigation.onBeforeNavigate.addListener((details) => {
    const { tabId, url } = details;
    console.log(url)

    // Send a request to the backend to check if the website should be blocked
    fetch(backendURL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ link: url })
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not OK');
            }
            return response.json();
        })
        .then(data => {
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
});


