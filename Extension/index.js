const realTimeToggle = document.getElementById('real_time_toggle')
const addBookmark = document.getElementById('add_bookmark')

// Todo: make a request on the backend and get if the real-time blocking is on or off.

realTimeToggle.addEventListener('change', function () {
    if (this.checked) {
        // Todo: if the user turned the switch on, make a request to change that in the backend.
    } else {
        const confirmation = confirm('Are you sure you want to turn off blocking? This action may expose you to potential risks. Proceed?')
        if (!confirmation) {
            this.checked = true
            return
        }
        // Todo: if the user turned the switch off, make a request to change that in the backend.
    }
})

addBookmark.addEventListener('click', function () {
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        const currentTab = tabs[0];
        const tabUrl = currentTab.url;
        console.log('Current tab URL:', tabUrl);

        // Todo: make a request to the backend to add tabUrl to the bookmarks.
    });
})