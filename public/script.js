const API_URL = "https://full-stack-backend-y51w.onrender.com";


// ==================== SIGNUP ====================

const signupForm = document.getElementById("signupForm");

if (signupForm) {
    signupForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        const name = document.getElementById("name").value.trim();
        const age = document.getElementById("age").value.trim();
        const address = document.getElementById("address").value.trim();
        const email = document.getElementById("email").value.trim();
        const mobile = document.getElementById("mobile").value.trim();
        const password = document.getElementById("password").value;

        const mobileError = document.getElementById("mobileError");

        if (mobile.length !== 10 || !/^\d+$/.test(mobile)) {
            mobileError.textContent = "Please enter valid number";
            return;
        }

        mobileError.textContent = "";

        if (!name || !age || !address || !email || !mobile || !password) {
            alert("Please fill all the fields.");
            return;
        }

        if (password.length < 8) {
            alert("Password must be at least 8 characters.");
            return;
        }

        try {
            const response = await fetch(`${API_URL}/signup`, {
                method: "POST",
                credentials: "include",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    name: name,
                    age: age,
                    address: address,
                    email: email,
                    mobile: mobile,
                    password: password
                })
            });

            const result = await response.json();

            if (result.success) {
                alert("Account created successfully!");
                window.location.href = "/login.html";
            } else {
                alert(result.message);
            }

        } catch (error) {
            console.error(error);
            alert("Unable to connect to the backend.");
        }
    });
}


// ==================== LOGIN ====================

const loginForm = document.getElementById("loginForm");

if (loginForm) {
    loginForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value;

        if (!email || !password) {
            alert("Please enter email and password.");
            return;
        }

        try {
            const response = await fetch(`${API_URL}/login`, {
                method: "POST",
                credentials: "include",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    email: email,
                    password: password
                })
            });

            const result = await response.json();

            if (result.success) {
                alert("Login successful!");
                window.location.href = "/dashboard.html";
            } else {
                alert(result.message);
            }

        } catch (error) {
            console.error(error);
            alert("Unable to connect to the backend.");
        }
    });
}


// ==================== DOWNLOAD ====================

const downloadBtn = document.getElementById("downloadBtn");

if (downloadBtn) {
    downloadBtn.addEventListener("click", function () {

        window.location.href =
            `${API_URL}/download?filename=test_file.txt`;

    });
}

// ==================== UPLOAD ====================

const uploadForm = document.getElementById("uploadForm");

if (uploadForm) {
    uploadForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        const file1 = document.getElementById("file1").files[0];
        const file2 = document.getElementById("file2").files[0];

        if (!file1 || !file2) {
            alert("Please select both files.");
            return;
        }

        const formData = new FormData();

        formData.append("file1", file1);
        formData.append("file2", file2);

        try {
            const response = await fetch(`${API_URL}/upload`, {
                method: "POST",
                credentials: "include",
                body: formData
            });

            const result = await response.json();

            if (result.success) {
                alert("Files uploaded successfully!");
            } else {
                alert(result.message);
            }

        } catch (error) {
            console.error(error);
            alert("Unable to connect to the backend.");
        }
    });
}


// ==================== LOGOUT ====================

const logoutBtn = document.getElementById("logoutBtn");

if (logoutBtn) {
    logoutBtn.addEventListener("click", async function () {

        try {
            const response = await fetch(`${API_URL}/logout`, {
                method: "GET",
                credentials: "include"
            });

            const data = await response.json();

            if (data.success) {
                window.location.href = "/login.html?logout=success";
            }

        } catch (error) {
            console.error(error);
            alert("Unable to logout.");
        }
    });
}


// ==================== FORGOT PASSWORD ====================

const forgotPasswordForm = document.getElementById("forgotPasswordForm");

if (forgotPasswordForm) {

    forgotPasswordForm.addEventListener("submit", async function (event) {

        event.preventDefault();

        const email = document.getElementById("forgotEmail").value.trim();
        const newPassword = document.getElementById("newPassword").value;
        const confirmPassword = document.getElementById("confirmPassword").value;

        const alertBox = document.getElementById("forgotAlert");

        if (!email || !newPassword || !confirmPassword) {
            alertBox.textContent = "All fields are required.";
            alertBox.style.display = "block";
            return;
        }

        if (newPassword.length < 6) {
            alertBox.textContent = "Password must be at least 6 characters.";
            alertBox.style.display = "block";
            return;
        }

        if (newPassword !== confirmPassword) {
            alertBox.textContent = "Passwords do not match.";
            alertBox.style.display = "block";
            return;
        }

        try {

            const response = await fetch(`${API_URL}/forgot-password`, {
                method: "POST",
                credentials: "include",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    email: email,
                    newPassword: newPassword
                })
            });

            const data = await response.json();

            alertBox.textContent = data.message;
            alertBox.style.display = "block";

            if (data.success) {

                alertBox.classList.add("password-success");

                setTimeout(() => {
                    window.location.href = "/login.html";
                }, 3000);
            }

        } catch (error) {

            console.error(error);

            alertBox.textContent =
                "Something went wrong. Please try again.";

            alertBox.style.display = "block";
        }

    });

}
// ==================== LOAD USER NAME ====================

const userName = document.getElementById("userName");
const welcomeName = document.getElementById("welcomeName");

if (userName || welcomeName) {

    fetch(`${API_URL}/current-user`, {
        method: "GET",
        credentials: "include"
    })
    .then(response => response.json())
    .then(data => {

        if (data.success) {

            if (userName) {
                userName.textContent = data.user_name;
            }

            if (welcomeName) {
                welcomeName.textContent = data.user_name;
            }

        } else {
            console.log("User not logged in");
        }

    })
    .catch(error => {
        console.error("Error loading user:", error);
    });
}