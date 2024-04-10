
// document.getElementById('demo-button').addEventListener('click', function () {
//     fetch('/authenticate/read_email/')
//         .then(response => {
//             if (!response.ok) {
//                 throw new Error('Network response was not ok');
//             }
//             return response.json(); // Assuming your Django view returns JSON
//         })
//         .then(data => {
//             console.log(data); // Process your response data here
//         })
//         .catch(error => {
//             console.error('Fetch error:', error);
//         });
// });

document.getElementById('demo-button').addEventListener('click', function () {
    window.location.href = '/user/login';
});
//   