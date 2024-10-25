

// function togglePasswordVisibility() {
//     const passwordInput = document.getElementById('password');
//     const toggleIcon = document.getElementById('toggleIcon');
//     if (passwordInput.type === 'password') {
//         passwordInput.type = 'text';
//         toggleIcon.classList.remove('fa-eye');
//         toggleIcon.classList.add('fa-eye-slash');
//     } else {
//         passwordInput.type = 'password';
//         toggleIcon.classList.remove('fa-eye-slash');
//         toggleIcon.classList.add('fa-eye');
//     }
// }

// document.getElementById("placeholder").onclick = function () {
//     document.getElementById("profilePictureInput").click();
// };

// Function to display the selected image before submitting
// document.addEventListener('DOMContentLoaded', function() {
//     function previewProfilePicture(event) {
//         const reader = new FileReader();
//         reader.onload = function () {
//             const output = document.getElementById("profilePicturePreview");
//             output.src = reader.result;
//             document.getElementById("profilePicturePreview").style.display = "block";
//         };
//         reader.readAsDataURL(event.target.files[0]);
//     }

//     // Ensure the input field exists before attaching the event listener
//     const profileInput = document.getElementById('profilePictureInput');
//     if (profileInput) {
//         profileInput.addEventListener('change', previewProfilePicture);
//     }
// });

