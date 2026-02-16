async function loadUserHistory() {
    const email = localStorage.getItem("userEmail");
    if (!email) return;

    const res = await fetch(`/user-data/${email}`);
    const data = await res.json();

    const tbody = document.getElementById("history");
    tbody.innerHTML = "";

    if (data.length === 0) {
        tbody.innerHTML = "<tr><td colspan='4'>No predictions yet</td></tr>";
        return;
    }

    data.forEach(r => {
        const row = `
            <tr>
                <td>${new Date(r.created_at).toLocaleString()}</td>
                <td>${Math.round(r.probability * 100)}%</td>
                <td><span class="badge ${r.risk.toLowerCase()}">${r.risk}</span></td>
                <td>${r.suggestion || "-"}</td>
            </tr>
        `;
        tbody.innerHTML += row;
    });

    renderUserChart(data.slice(0, 10).reverse());
}

function renderUserChart(data) {
    const ctx = document.getElementById("userChart");
    if (!ctx) return;

    new Chart(ctx, {
        type: "line",
        data: {
            labels: data.map((_, i) => i + 1),
            datasets: [{
                label: "Churn Probability %",
                data: data.map(r => Math.round(r.probability * 100)),
                borderColor: "#38bdf8",
                tension: 0.4
            }]
        }
    });
}

document.addEventListener("DOMContentLoaded", loadUserHistory);
