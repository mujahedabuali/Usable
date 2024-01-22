document.addEventListener('DOMContentLoaded', function () {
    const urlParams = new URLSearchParams(window.location.search);
    const data = JSON.parse(decodeURIComponent(urlParams.get('data')));

    const isSSLText = document.getElementById('isSSLText')
    isSSLText.textContent = `SSL certificate: ${data.isSSL ? 'Enabled' : 'No certificate'}`
    if (data.isSSL) {
        isSSLText.style.textDecorationColor = '#51ff00'
    } else {
        isSSLText.style.textDecorationColor = '#ff0000'
    }

    const isSSLExpiredText = document.getElementById('isExpiredSSLText')
    isSSLExpiredText.textContent = `SSL expiration: ${data.isExpiredSSL ? 'Expired' : 'Not expired'}`
    if (data.isExpiredSSL) {
        isSSLExpiredText.style.textDecorationColor = '#ff0000'
    } else {
        isSSLExpiredText.style.textDecorationColor = '#51ff00'
    }

    const ageText = document.getElementById('ageText')
    ageText.textContent = `Domain age: ${data.age} Years`
    if (data.age >= 3) {
        ageText.style.textDecorationColor = '#00ff00'
    } else {
        ageText.style.textDecorationColor = '#ff0000'
    }

    const warningsList = document.getElementById('warningsList')
    if (data.warnings.length > 0) {
        data.warnings.forEach(warning => {
            const li = document.createElement('li');
            li.textContent = warning;
            warningsList.appendChild(li);
        });
    } else {
        warningsList.textContent = 'No warnings';
    }
});
