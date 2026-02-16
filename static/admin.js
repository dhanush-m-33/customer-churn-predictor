document.addEventListener("DOMContentLoaded", loadAdminData);

async function loadAdminData() {
    const res = await fetch("/admin-data");
    const data = await res.json();

    document.getElementById("usersCount").innerText =
        data.last_30_days_users_count;

    document.getElementById("overall").innerText =
        Math.round(data.overall * 100) + "%";

    const tbody = document.getElementById("adminHistory");
    tbody.innerHTML = "";

    data.history.forEach(r => {
        const row = `
            <tr>
                <td>${r.user}</td>
                <td>${new Date(r.created_at).toLocaleString()}</td>
                <td>${Math.round(r.probability * 100)}%</td>
                <td><span class="badge ${r.risk.toLowerCase()}">${r.risk}</span></td>
                <td>${r.suggestion || "-"}</td>
            </tr>
        `;
        tbody.innerHTML += row;
    });

    renderAdminChart(data.history.slice(0, 10).reverse());
}

function renderAdminChart(data) {
    const ctx = document.getElementById("adminChart");

    new Chart(ctx, {
        type: "bar",
        data: {
            labels: data.map((_, i) => i + 1),
            datasets: [{
                label: "Churn %",
                data: data.map(r => Math.round(r.probability * 100)),
                backgroundColor: "#ef4444"
            }]
        }
    });
}

function logout() {
    localStorage.clear();
    window.location.href = "/";
}
