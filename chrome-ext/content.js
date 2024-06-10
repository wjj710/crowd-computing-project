const GPTSM_ENDPOINT = "http://127.0.0.1:5000/";

updatePage();

function updatePage() {
    console.log("updatePage");
    var elements = document.getElementsByTagName('p');
    var l = elements.length;

    var plain_text = new Array(l);
    for (var i = 0; i < l; i++) {
        plain_text[i] = elements[i].innerText;
    }
    requestGPTSM(l, elements, plain_text);
}

function requestGPTSM(l, elements, plain_text) {
    var fd = new FormData();
    fd.append("payload", JSON.stringify(plain_text));

    fetch(GPTSM_ENDPOINT, {
        method: "POST",
        body: fd
    })
    .then(response => response.json())
    .then((json) => {
        console.log(json);
        styled_text = json['payload'];
        for (var i = 0; i < l; i++) {
            elements[i].innerHTML = styled_text[i];
        }
    });
}