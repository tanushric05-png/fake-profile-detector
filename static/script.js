
document.getElementById("profileForm")?.addEventListener("submit", function(e) {
    e.preventDefault();

    let followers = document.getElementById("followers").value;
    let following = document.getElementById("following").value;
    let posts = document.getElementById("posts").value;

    fetch("/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            followers: followers,
            following: following,
            posts: posts
        })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("result").innerHTML = data.prediction;
    });
});