// ---------- RECENT SEARCH STORAGE ----------

function saveRecent(username) {

    let list = JSON.parse(
        localStorage.getItem("recentUsers") || "[]"
    );

    if (!list.includes(username)) {
        list.unshift(username);
    }

    list = list.slice(0, 5);

    localStorage.setItem(
        "recentUsers",
        JSON.stringify(list)
    );
}

function loadRecent() {

    let list = JSON.parse(
        localStorage.getItem("recentUsers") || "[]"
    );

    let container =
        document.getElementById("recentList");

    if (!container) return;

    container.innerHTML = "";

    list.forEach(user => {

        let div = document.createElement("div");

        div.className = "recent-item";
        div.textContent = user;

        div.onclick = () => {
            document.getElementById("username").value = user;
        };

        container.appendChild(div);
    });
}

window.onload = loadRecent;


// ---------- SAVE ON FORM SUBMIT ----------

document.addEventListener("DOMContentLoaded", () => {

    let form = document.querySelector(".search-form");

    if (!form) return;

    form.addEventListener("submit", () => {

        let username =
            document.getElementById("username").value;

        saveRecent(username);
    });
});