const realTimeToggle = document.getElementById('real_time_toggle')
const addBookmark = document.getElementById('add_bookmark')

// Todo: make a request on the backend and get if the real-time blocking is on or off.



addBookmark.addEventListener('click', function () {
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        const currentTab = tabs[0];
        const tabUrl = currentTab.url;
        console.log('Current tab URL:', tabUrl);

        // Todo: make a request to the backend to add tabUrl to the bookmarks.
    });
})