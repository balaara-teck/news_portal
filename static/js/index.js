

function togglePasswordVisibility() {
    const passwordInput = document.getElementById('password');
    const toggleIcon = document.getElementById('toggleIcon');
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        toggleIcon.classList.remove('fa-eye');
        toggleIcon.classList.add('fa-eye-slash');
    } else {
        passwordInput.type = 'password';
        toggleIcon.classList.remove('fa-eye-slash');
        toggleIcon.classList.add('fa-eye');
    }
}

document.getElementById("placeholder").onclick = function () {
    document.getElementById("profilePictureInput").click();
};

// Function to display the selected image before submitting
function previewProfilePicture(event) {
    const reader = new FileReader();
    reader.onload = function () {
        const output = document.getElementById("profilePicturePreview");
        const placeholder = document.getElementById("placeholder");
        output.src = reader.result;
        output.style.display = "block"; // Show the uploaded image
        placeholder.style.display = "none"; // Hide the placeholder
    };
    reader.readAsDataURL(event.target.files[0]);
