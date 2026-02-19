document.addEventListener("DOMContentLoaded", loadAdminData);

async function loadAdminData() {
    const res = await fetch("/admin-data");
    const data = await res.json();

    document.getElementById("totalUsers").innerText =
        data.total_users;

    document.getElementById("totalPredictions").innerText =
        data.total_predictions;

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

function exportCSV() {
    window.location.href = "/export-last-30-days";
}

async function uploadBulkFile() {

    const fileInput = document.getElementById("bulkFile");
    const file = fileInput.files[0];

    if (!file) {
        alert("Please select a CSV file");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch("/bulk-predict", {
        method: "POST",
        body: formData
    });

    const data = await res.json();

    if (!res.ok) {
        alert(data.error);
        return;
    }

    const tbody = document.getElementById("bulkResults");
    tbody.innerHTML = "";

    data.results.forEach(r => {
        const row = `
            <tr>
                <td>${r.user}</td>
                <td>${Math.round(r.probability * 100)}%</td>
                <td><span class="badge ${r.risk.toLowerCase()}">${r.risk}</span></td>
            </tr>
        `;
        tbody.innerHTML += row;
    });

    document.getElementById("bulkSummary").innerHTML = `
        <h4>Overall Average Churn Probability: 
        <span style="color:#38bdf8;">
        ${Math.round(data.overall_probability * 100)}%
        </span></h4>
    `;
}
