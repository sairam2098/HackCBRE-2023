function showInsights() {
    const urlParams = new URLSearchParams(window.location.search);
    var userEmail = urlParams.get('email');
    var userNameMapping = {
        'christinebird@watson.com': 'Carl Ramirez',
        'yhenry@williams.com': 'Lisa Hoffman'
    };

    var user_name = userNameMapping[userEmail]

    if (user_name) {
        document.getElementById('userRole').textContent = 'Welcome ' + user_name + '';
    } else {
        document.getElementById('userRole').textContent = 'User not found';
    }


    fetch('http://localhost:8000/insights?' + new URLSearchParams({
        name: user_name
    }))
    .then(response => {
        if(response.ok) {
            return response.json();
        }else {
            throw new Error('Api call failed');
        }
    })
    .then(data => {
        console.log(data);
        const outputElement = document.getElementById('output');

        data.forEach(item => {
            const div = document.createElement('div');

            div.innerHTML = `
                <strong>Criticality:</strong> ${item.Criticality}<br>
                <strong>Driver:</strong> ${item.Driver}<br>
                <strong>Property Address:</strong> ${item['Property Address']}<br>
            `;

            div.classList.add('data-block');

            outputElement.appendChild(div);
        });
    })
    .catch(error => {
        console.error(error)
    })
}