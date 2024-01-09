const realTimeToggle = document.getElementById('real_time_toggle')
const addBookmark = document.getElementById('add_bookmark')


addBookmark.addEventListener('click', function () {
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        if (tabs) {
            const currentTab = tabs[0];
            const tabUrl = currentTab.url;
            const name = currentTab.title;

            sendDataToBackend(tabUrl, name);
        }
    });
})

function sendDataToBackend(url, title) {
    const backendUrl = 'http://localhost:8000/add_bookmark'
    const data = {
        name: title,
        url: url
    }

    fetch(backendUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then(response => {
            if (response.ok) {
                return response.json();
            }
            throw new Error('Network response was not OK');
        })
        .then(result => {
            console.log('Bookmark added:', result);
        })
        .catch(error => {
            console.error('Error:', error);
        });
}