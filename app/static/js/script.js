function initFormSubmission() {
    const form = document.getElementById('realestate-form');

    const throbber = document.getElementById('throbber');
    
    const result_location = document.getElementById('result-location');
    const result_city = document.getElementById('result-city');
    const result_rubric = document.getElementById('result-rubric');
    const result_num = document.getElementById('result-num');
    const result_error = document.getElementById('result-error');
    const result = document.getElementById('result');
    
    result.style.display = 'none';

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        form.style.display = 'none';

        throbber.style.display = 'block';

        const city = document.querySelector('input[name="city"]').value;

        try{
            const response = await fetch('/realestate', {
                method: 'POST',
                headers: {
                    "Accept": "application/json",
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    city: city 
                }),
            });

            throbber.style.display = 'none';

            if (document.mozHidden !== undefined) {
                document.mozHidden = false;
            }
            
            if (response.ok){
                const data = await response.json();

                window.history.pushState({}, null, response.url);

                result.style.display = 'block';
                
                result_city.textContent = data.city;
                result_rubric.textContent = data.rubric;
                result_num.textContent = data.num;
                result_error.textContent = data.error;

            } else if (response.status === 500) {
                window.location.href = '/error';
            }
            
        } catch (err) {
            window.location.href = '/error';
        }
    });
}


function clearElement() {
    window.addEventListener('popstate', function(event) {
        document.getElementById('realestate-form').reset();
    
        document.getElementById('result').innerHTML = '';
        document.getElementById('result-location').innerHTML = '';
        document.getElementById('result-city').innerHTML = '';
        document.getElementById('result-rubric').innerHTML = '';
        document.getElementById('result-num').innerHTML = '';
        document.getElementById('result-error').innerHTML = '';
    });
    return true;
}


clearElement();

initFormSubmission();
