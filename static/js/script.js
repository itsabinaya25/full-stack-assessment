const signupForm = document.getElementById("signupForm");

if (signupForm) {
    signupForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        // Get values
        const name = document.getElementById("name").value.trim();
        const age = document.getElementById("age").value.trim();
        const address = document.getElementById("address").value.trim();
        const email = document.getElementById("email").value.trim();
        const mobile = document.getElementById("mobile").value.trim();
        const password = document.getElementById("password").value;

        // Basic validation
        if (!name || !age || !address || !email || !mobile || !password) {
            alert("Please fill all the fields.");
            return;
        }

        if (password.length < 8) {
            alert("Password must be at least 8 characters.");
            return;
        }
           const response = await fetch("/signup", {
            method: "POST",
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
            window.location.href = "/login";
        } else {
            alert(result.message);
        }
    });
}


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

        const response = await fetch("/login", {
            method: "POST",
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
            window.location.href = "/dashboard";
        } else {
            alert(result.message);
        }
    });
}


const downloadBtn = document.getElementById("downloadBtn");

if (downloadBtn) {
    downloadBtn.addEventListener("click", function () {
        window.location.href = "/download";
    });
}


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

        const response = await fetch("/upload", {
            method: "POST",
            body: formData
        });

        const result = await response.json();

        if (result.success) {
            alert("Files uploaded successfully!");
        } else {
            alert(result.message);
        }
    });
}