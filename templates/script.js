window.onload = function() {
    fetch('/report')
    .then(response => response.json())
    .then(data => {
        const feedbackList = document.getElementById('feedback-list');
        data.forEach(feedback => {
            const feedbackItem = document.createElement('div');
            feedbackItem.classList.add('feedback-item');
            feedbackItem.innerHTML = `
                <p><strong>Bus Route:</strong> ${feedback.bus_route}</p>
                <p><strong>Driver Behaviour:</strong> ${feedback.driver_behaviour}</p>
                <p><strong>Bus Condition:</strong> ${feedback.bus_condition}</p>
                <p><strong>General Behaviour:</strong> ${feedback.general_behaviour}</p>
            `;
            feedbackList.appendChild(feedbackItem);
        });
    })
    .catch(error => console.error('Error fetching data:', error));
};
