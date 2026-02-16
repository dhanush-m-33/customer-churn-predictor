document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("prediction-form");

    if (!form) return;

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const email = localStorage.getItem("userEmail");

        const inputs = {
            tenure: document.getElementById("tenure").value,
            watch_hours: document.getElementById("watch_hours").value,
            days_since_login: document.getElementById("days_since_login").value,
            subscription_type: document.getElementById("subscription_type").value,
            tickets_raised: document.getElementById("tickets_raised").value,
            profiles_used: document.getElementById("profiles_used").value
        };

        const res = await fetch("/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, inputs })
        });

        const data = await res.json();

        updateProbabilityBar(data.probability);
        loadUserHistory();
    });
});

function updateProbabilityBar(prob) {
    const bar = document.getElementById("probBar");
    const percent = Math.round(prob * 100);

    bar.style.width = percent + "%";
    bar.innerText = percent + "%";

    bar.className = "progress-bar";

    if (percent > 70) bar.classList.add("high");
    else if (percent > 40) bar.classList.add("medium");
    else bar.classList.add("low");
}
