const realTimeToggle = document.getElementById('real_time_toggle')
const addBookmark = document.getElementById('add_bookmark')
const checkWebsite = document.getElementById('check_website')
const gauge = document.getElementById('gauge')
const gaugeFill = document.getElementById('fill')
const gaugeCover = document.getElementById('cover')
const errorIndecator = document.getElementById('errorIndecator')
const details = document.getElementById('details')
const meaning = document.getElementById('meaning')
const techDetails = document.getElementById('techDetails')
const loaderContainer = document.getElementsByClassName('loader-container')[0]
const usernameInput = document.getElementById('username');
const passwordInput = document.getElementById('password');
const submitButton = document.getElementById('submit');
const mainContainer = document.getElementsByClassName('main-container')[0]
const loginContainer = document.getElementsByClassName('login-container')[0]
const logoutButton = document.getElementById('logoutButton')

document.addEventListener('DOMContentLoaded', function () {
    chrome.storage.local.get(['sessionKey'], function (result) {
        const sessionKey = result.sessionKey;

        if (sessionKey) {
            mainContainer.style.display = 'block'
            loginContainer.style.display = 'none'
        }
    });
});

logoutButton.addEventListener('click', function () {
    chrome.storage.local.remove('sessionKey', function () {
        console.log('Logout');
        chrome.runtime.reload();
    });
})


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

checkWebsite.addEventListener('click', function () {
    checkWebsite.disabled = true
    checkWebsite.style.color = '#7aff9c'
    checkWebsite.style.cursor = 'not-allowed'
    checkWebsite.style.border = '2px solid #7aff9c'
    loaderContainer.style.display = 'flex'
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        if (tabs) {
            const currentTab = tabs[0];
            const url = currentTab.url;
            const name = currentTab.title;
            const domainName = extractDomainName(url)
            checkTrustworthiness(domainName)

        }

    });

});

meaning.addEventListener('click', function () {
    window.open('meaning.html', '_blank')
})

function checkTrustworthiness(domainName) {
    let numberOfWarnings = 0
    let isSSL
    let isExpiredSSL = true
    let age

    const apiKey = 'at_1rz2ZoDfaViZzJiYfqyUhNme09x6J'
    let apiUrl = 'https://domain-reputation.whoisxmlapi.com/api/v2'
    let fullUrl = `${apiUrl}?apiKey=${apiKey}&domainName=${domainName}&mode=full&outputFormat=JSON`

    // Get the domain warnings
    fetch(fullUrl)
        .then(response => {
            if (!response.ok) {
                console.log('HTTP Error while getting Reputation:' + response.status)
                loaderContainer.style.display = 'none'
                return
            }
            return response.json()
        })
        .then(data => {
            let warnings = []

            for (let i = 0; i < data.testResults.length; i++) {
                for (let j = 0; j < data.testResults[i].warnings.length; j++) {
                    numberOfWarnings++
                    warnings.push(data.testResults[i].warnings[j].warningDescription)
                }
            }

            // check if the SSL certificate is expired or not
            apiUrl = 'https://ssl-certificates.whoisxmlapi.com/api/v1'
            fullUrl = `${apiUrl}?apiKey=${apiKey}&domainName=${domainName}&outputFormat=JSON&hardRefresh=1`

            fetch(fullUrl)
                .then(response => {
                    if (!response.ok) {
                        console.log('HTTP Error while getting SSL:' + response.status)
                        loaderContainer.style.display = 'none'
                        return
                    }
                    return response.json()
                })
                .then(data => {
                    if (!data.certificates[0]) {
                        isSSL = false
                    } else {
                        isSSL = true;
                        const expireDateString = data.certificates[0].validTo
                        const expireDate = new Date(expireDateString);
                        const currentDate = new Date();
                        if (expireDate < currentDate) {
                            isExpiredSSL = true
                        } else {
                            isExpiredSSL = false
                        }
                    }

                    // check the domain age
                    apiUrl = 'https://www.whoisxmlapi.com/whoisserver/WhoisService'
                    fullUrl = `${apiUrl}?domainName=${domainName}&apiKey=${apiKey}&outputFormat=JSON&_hardRefresh=1`
                    fetch(fullUrl)
                        .then(response => {
                            if (!response.ok) {
                                console.log('HTTP Error while getting Domain Age:' + response.status)
                                loaderContainer.style.display = 'none'
                                return
                            }
                            return response.json()
                        })
                        .then(data => {
                            let dateString
                            let isThereAge = true
                            console.log(data)
                            if (data.WhoisRecord.createdDate) {
                                dateString = data.WhoisRecord.createdDate
                            } else if (data.WhoisRecord.registryData.createdDate) {
                                dateString = data.WhoisRecord.registryData.createdDate
                            } else {
                                isThereAge = false
                            }

                            console.log(dateString)
                            const date = new Date(dateString)
                            console.log(date)
                            const currentDate = new Date()
                            console.log(currentDate)
                            const timeDifference = currentDate - date;
                            const millisecondsInYear = 1000 * 60 * 60 * 24 * 365.25;
                            const yearsDifference = timeDifference / millisecondsInYear;
                            console.log(yearsDifference)
                            if (isThereAge) {
                                age = Math.floor(yearsDifference);
                            } else {
                                age = -1
                            }

                            const trustEvaluation = evaluateTrust(isSSL, isExpiredSSL, age, numberOfWarnings)
                            console.log(isSSL + '  ' + isExpiredSSL + '  ' + age + '  ' + numberOfWarnings)
                            console.log(trustEvaluation)

                            if (trustEvaluation == -1) {
                                errorIndecator.classList.add('visible')
                                loaderContainer.style.display = 'none'
                                checkWebsite.disabled = false
                                checkWebsite.style.color = '#00ff40'
                                checkWebsite.style.cursor = 'pointer'
                                checkWebsite.classList.add('check_website:hover')
                                checkWebsite.addEventListener('mouseover', function () {
                                    checkWebsite.style.color = 'black'
                                })
                            } else {
                                // document.body.style.height = '47em';
                                gauge.classList.add('visible');
                                loaderContainer.style.display = 'none'
                                setGaugeFill(trustEvaluation / 100)
                                checkWebsite.disabled = false
                                checkWebsite.style.color = '#00ff40'
                                checkWebsite.style.cursor = 'pointer'
                                details.classList.add('visible')
                                checkWebsite.addEventListener('mouseover', function () {
                                    checkWebsite.style.color = 'black'
                                })

                                techDetails.addEventListener('click', function () {
                                    chrome.runtime.sendMessage({
                                        action: "openTechDetailsTab",
                                        data: {
                                            isSSL: isSSL,
                                            isExpiredSSL: isExpiredSSL,
                                            age: age,
                                            warnings: warnings
                                        }
                                    });
                                });
                            }
                        })
                        .catch(error => {
                            console.log('Error' + error)
                            loaderContainer.style.display = 'none'
                        })
                })
                .catch(error => {
                    console.log('Error' + error)
                    loaderContainer.style.display = 'none'
                })
        })
        .catch(error => {
            console.log('Error' + error)
            loaderContainer.style.display = 'none'
        })




}

function evaluateTrust(isSSL, isExpiredSSL, age, warningsNumber) {

    if (age == -1) {
        return -1
    }

    let evaluation = 0

    if (isSSL) {
        evaluation += 40
    }
    if (!isExpiredSSL) {
        evaluation += 20
    } else {
        evaluation -= 10
    }
    if (age < 1) {
        evaluation += 5
    } else if (age >= 1 && age < 3) {
        evaluation += 20
    } else if (age >= 3 && age < 5) {
        evaluation += 30
    } else if (age > 5) {
        evaluation += 40
    }


    evaluation -= warningsNumber

    if (evaluation < 5) {
        evaluation = 5
    }
    return evaluation
}

function extractDomainName(url) {
    const newUrl = new URL(url)
    return newUrl.hostname
}

function sendDataToBackend(url, title) {
    const backendUrl = 'http://localhost:8000/add_bookmark'
    chrome.storage.local.get(['sessionKey'], function (result) {
        const sessionKey = result.sessionKey

        const data = {
            name: title,
            url: url,
            sessionID: sessionKey
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
    });

}

function setGaugeFill(value) {
    gaugeFill.style.transform = `rotate(${value / 2}turn)`
    gaugeCover.textContent = `${Math.round(value * 100)}%`
    if (value <= 1 && value >= 0.85) {
        gaugeFill.style.background = '#09ce26'
        gaugeCover.style.color = '#09ce26'
    } else if (value < 0.85 && value >= 0.7) {
        gaugeFill.style.background = '#f3ef00'
        gaugeCover.style.color = '#f3ef00'
    } else if (value < 0.7) {
        gaugeFill.style.background = '#e00000'
        gaugeCover.style.color = '#e00000'
    }
}

// login code


submitButton.addEventListener('click', function () {
    const username = usernameInput.value;
    const password = passwordInput.value;
    console.log(username + '  ' + password);

    fetch('http://localhost:8000/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
    })
        .then(response => {
            if (response.ok) {
                // Return the parsed JSON from the response
                return response.json();
            } else {
                if (response.status == 401) {
                    window.alert('Username or password is not correct!')
                    return
                }
            }
        })
        .then(result => {
            if (result.message == 'Login successful') {
                mainContainer.style.display = 'block'
                loginContainer.style.display = 'none'
                const sessionKey = result.session_id
                console.log(sessionKey + 'index.js')  // Replace this with the actual session key
                chrome.runtime.sendMessage({ action: "setSessionKey", sessionKey: sessionKey });
            } else {

            }

        })
        .catch(error => {
            // Handle any errors that occurred during the fetch
            console.error('Error:', error);
        });
});
