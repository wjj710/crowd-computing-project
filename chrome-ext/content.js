const GPTSM_ENDPOINT = "http://127.0.0.1:5000/";

// chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab) {
//     // TODO: use different template for different URLs
//     // if (changeInfo.url) {
//     //     chrome.tabs.sendMessage(tabId, { tabChanged: true, title: tab.url });
//     // }
//     onNewPage();
// });

onNewPage();

function onNewPage() {
    console.log("onNewPage");
    var paragraphs = document.getElementsByTagName('p');
    var l = paragraphs.length;
    var plain_text = new Array(l);

    for (var i = 0; i < l; i++) {
        plain_text[i] = paragraphs[i].innerText;
    }

    requestGPTSM(l, paragraphs, plain_text);
}

function requestGPTSM(l, paragraphs, plain_text) {
    var fd = new FormData();
    fd.append("payload", plain_text);

    fetch(GPTSM_ENDPOINT, {
        method: "POST",
        body: fd
    })
    .then((response) => response.json())
    .then((json) => {
        console.log(json);
        // updatePage(paragraphs, json);
    });

    // var styled_text = new Array(l);
    // for (var i = 0; i < l; i++) {
    //     level = Math.floor(Math.random() * 5);
    //     styled_text[i] = `<span class="gptsm-l${level}">${plain_text[i]}</>`;
    // }

    // updatePage(l, paragraphs, styled_text)
}

function updatePage(l, paragraphs, styled_text) {
    for (var i = 0; i < l; i++) {
        paragraphs[i].innerHTML = styled_text[i];
    }
}