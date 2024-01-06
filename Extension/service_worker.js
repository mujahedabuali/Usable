const apiKey = 'AIzaSyD_sBfydgE1kbg5y1xAPKJFRXZB8hH4fQc' // this is the api key for google safe browsing api
const backendURL = 'http://localhost:8000/add_blocked_site'


// this method is going to run when the user visits any website (the code will run before the website is fully visited)
chrome.webNavigation.onBeforeNavigate.addListener((details) => {

    // Todo: query the backend database to check if the real-time blocking is on or off.

    // details are details about the website that the user is trying to visit
    const { tabId, url } = details;


    // after getting the URL of the website, we want to check if its safe
    // we will do so by using google safe browsing api, we will sent the url for the api.
    // 'MALWARE and SOCIAL_ENGINEERING are the things we are checking if the website related to.
    fetch(`https://safebrowsing.googleapis.com/v4/threatMatches:find?key=${apiKey}`, {
        method: 'POST',
        body: JSON.stringify({
            client: {
                clientId: 'MyExtension',
                clientVersion: '1.0.0'
            },
            threatInfo: {
                threatTypes: ['MALWARE', 'SOCIAL_ENGINEERING', 'UNWANTED_SOFTWARE', 'POTENTIALLY_HARMFUL_APPLICATION'],
                platformTypes: ['ANY_PLATFORM'],
                threatEntryTypes: ['URL'],
                threatEntries: [{ 'url': url }]
            }
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then(response => {
            // This code runs if the response failed
            if (!response.ok) {
                throw new Error('Network response was not OK');
            }
            return response.json(); // Parse response as JSON
        })
        .then(data => {
            // This code runs when the api successfully responded.
            // First we check if the response is empty or not.
            // if the response is empty, it means that the website did not match any criteria we are looking for (malware, social engineering..etc)
            // if the response is not empty, it means that the website has something we are looking for and the details will be presented in the response.
            let matches = data.matches || [];
            if (matches.length > 0) {
                let cause
                if (matches[0].threatType == 'SOCIAL_ENGINEERING') {
                    cause = 'Phishing website (Some one is trying to steel your information)'
                } else if (matches[0].threatType == 'POTENTIALLY_HARMFUL_APPLICATION') {
                    cause = 'HARMFUL APPLICATION'
                } else {
                    cause = matches[0].threatType.replace('_', ' ')
                }
                // send the url to the backend
                fetch(backendURL, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ url: url })
                })
                    .then(response => {
                        console.log('request sent successfully')
                    })
                    .catch(error => {
                        console.error('Error:', error)
                    })
                let redirectURL = chrome.runtime.getURL(`blocked.html?data=${encodeURIComponent(url)}&cause=${encodeURIComponent(cause)}`)
                chrome.tabs.update(tabId, { url: redirectURL })

            }
        })
        .catch(error => {
            console.error('Error:', error);
        });

    let domain = new URL(url).hostname
    console.log(domain)
    //chrome.tabs.update(tabId, { url: chrome.runtime.getURL('delay.html') });

}, { url: [{ schemes: ['http', 'https'] }] });
