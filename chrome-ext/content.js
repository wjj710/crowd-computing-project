const GPTSM_ENDPOINT = "http://127.0.0.1:5000/";

updatePage();

function updatePage() {
    console.log("updatePage");
    var elements = document.getElementsByTagName('p');
    var l = elements.length;

    for (var i = 0; i < l; i++) {
        requestGPTSM(elements[i], elements[i].innerText);
    }
}

function requestGPTSM(p, plain_text) {
    var fd = new FormData();
    fd.append("payload", plain_text);

    fetch(GPTSM_ENDPOINT, {
        method: "POST",
        body: fd
    })
    .then(response => response.json())
    .then((json) => {
        console.log(json);
        p.innerHTML = json['payload'];
    });
}