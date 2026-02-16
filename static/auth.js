document.addEventListener("DOMContentLoaded", () => {

    // Protect user page
    if (window.location.pathname === "/user") {
        const role = localStorage.getItem("userRole");
        if (!role || role !== "user") {
            window.location.replace("/");
        }
    }

    // Protect admin page
    if (window.location.pathname === "/admin") {
        const role = localStorage.getItem("userRole");
        if (!role || role !== "admin") {
            window.location.replace("/");
        }
    }


    // ---------------- LOGIN ----------------
    const loginForm = document.getElementById("login-form");

    if (loginForm) {
        loginForm.addEventListener("submit", async (e) => {
            e.preventDefault();

            const email = document.getElementById("email").value;
            const password = document.getElementById("password").value;

            const res = await fetch("/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, password })
            });

            const data = await res.json();

            if (data.success) {
                localStorage.setItem("userEmail", data.email);
                localStorage.setItem("userRole", data.role);

                if (data.role === "admin") {
                    window.location.href = "/admin";
                } else {
                    window.location.href = "/user";
                }
            } else {
                document.getElementById("login-error").innerText = data.error;
            }
        });
    }


    // ---------------- REGISTER ----------------
    const registerForm = document.getElementById("register-form");

    if (registerForm) {
        registerForm.addEventListener("submit", async (e) => {
            e.preventDefault();

            const name = document.getElementById("reg-name").value;
            const email = document.getElementById("reg-email").value;
            const password = document.getElementById("reg-password").value;

            const res = await fetch("/register", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ name, email, password })
            });

            const data = await res.json();

            if (data.success) {
                alert("Registration successful! Please login.");
                registerForm.reset();
            } else {
                document.getElementById("register-error").innerText = data.error;
            }
        });
    }

});

function logout() {
    localStorage.removeItem("userEmail");
    localStorage.removeItem("userRole");
    window.location.replace("/");
}
