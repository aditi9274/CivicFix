const API = "http://127.0.0.1:5000";

const form = document.getElementById("issueForm");
const issuesDiv = document.getElementById("issues");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const issue = {
        category: category.value,
        location: location.value,
        description: description.value
    };

    await fetch(API + "/report", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(issue)
    });

    form.reset();
    loadIssues();
});

async function loadIssues() {
    const res = await fetch(API + "/issues");
    const data = await res.json();

    issuesDiv.innerHTML = "";

    data.forEach(issue => {
        issuesDiv.innerHTML += `
            <div class="issue">
                <b>${issue.category}</b> (${issue.location})<br>
                ${issue.description}<br>
                <small>Status: ${issue.status}</small>
            </div>
        `;
    });
}

loadIssues();
