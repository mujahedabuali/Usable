document.addEventListener('DOMContentLoaded', function () {
    const urlParams = new URLSearchParams(window.location.search);
    const url = urlParams.get('data');
    const cause = urlParams.get('cause')
    console.log(cause)

    const title = document.getElementById('title');
    const causeText = document.getElementById('cause')


    // Set the text content of the title with the span element included
    title.innerHTML = `The website: <span id="site-url">${url || 'No data passed'}</span> has been BLOCKED !`;
    const siteURL = document.getElementById('site-url');
    siteURL.classList.add('site-url');

    causeText.innerHTML = `Cause of blocking: potential ${cause}`

});
