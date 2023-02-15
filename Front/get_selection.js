function getText(e){
    // text is the raw text selected by the user, selected area is the html object, truetext is the data-JSONtimestamps value of the selected object
    var text, selected_area, truetext;
    console.log(e);
    text = (document.all) ? document.selection.createRange().text : document.getSelection().toString();
    selected_area = getSelectionBoundaryElement(true)[0];
    // console.log("function output:" + getSelectionBoundaryElement(true));
    selected_bounds = getSelectionBoundaryElement(true)[1];
    console.log(Object.getOwnPropertyNames(selected_bounds));
    selected_area_text = selected_area.textContent;
    non_selected_text = selected_area_text.substring(0, selected_bounds.startOffset) + selected_area_text.substring(selected_bounds.endOffset, selected_area_text.length)
    console.log("non selected text: " + non_selected_text);
    truetext = JSON.parse(selected_area.getAttribute("data-JSONtimestamps"));
    const timestamps = [];
    console.log("Text: " + text.split(" ") + "\nSelected boundary: " + selected_area + "\nTruetext: " + truetext);
    var startindex, endindex, indexval;
    startindex = 99999;
    endindex = -1;
    var wordcountdict = {}
    for (var i = 0; i < non_selected_text.split(" ").length; i++){
        if (!(non_selected_text.split(" ")[i] in wordcountdict)){
            wordcountdict[non_selected_text.split(" ")[i]] = 1;
        } else {
            wordcountdict[non_selected_text.split(" ")[i]] += 1;
        }
    }
    console.log(wordcountdict);
    // iterate over text, finding timestamps for each word
    for (var i = 0; i < text.split(" ").length; i++) {
        val = text.split(" ")[i];
        console.log(val + " " + i + " " + text.length);
        if (val in truetext){
            if (val in wordcountdict){
                indexval = truetext[val][wordcountdict[val]]
            } else {
                indexval = truetext[val][0]
            }
            console.log(truetext[val]);
            if (indexval < startindex){
                startindex = indexval;
            }
            if (indexval > endindex){
                endindex = indexval;
            }
        }
    }
    console.log(startindex + " " + endindex);


    // Change this
    socket = new WebSocket("ws://localhost:8765");
    socket.addEventListener('open', (event) => {
        // json string representing the timestamps to clip
        socket.send(`{"start_timestamp": ${startindex}, "end_timestamp": ${endindex}}`);
    });
}

// https://stackoverflow.com/questions/1335252/how-can-i-get-the-dom-element-which-contains-the-current-selection
function getSelectionBoundaryElement(isStart) {
    var range, sel, container;
    if (document.selection) {
        range = document.selection.createRange();
        range.collapse(isStart);
        return range.parentElement();
    } else {
        sel = window.getSelection();
        if (sel.getRangeAt) {
            if (sel.rangeCount > 0) {
                range = sel.getRangeAt(0);
            }
        } else {
            // Old WebKit
            range = document.createRange();
            range.setStart(sel.anchorNode, sel.anchorOffset);
            range.setEnd(sel.focusNode, sel.focusOffset);

            // Handle the case when the selection was selected backwards (from the end to the start in the document)
            if (range.collapsed !== sel.isCollapsed) {
                range.setStart(sel.focusNode, sel.focusOffset);
                range.setEnd(sel.anchorNode, sel.anchorOffset);
            }
       }

        if (range) {
           container = range[isStart ? "startContainer" : "endContainer"];

           // Check if the container is a text node and return its parent if so
           // console.log("from inside function:" + (container.nodeType === 3 ? container.parentNode : container) + "range: " + range);
           return [(container.nodeType === 3 ? container.parentNode : container), range];
        }   
    }
}

function getSelectedText() {
    var sel, text = "";
    if (window.getSelection) {
        text = "" + window.getSelection();
    } else if ( (sel = document.selection) && sel.type == "Text") {
        text = sel.createRange().text;
    }
    return text;
}

function testcase(){
    var docid = document.getElementById("transcript");
    console.log("docid: " + docid);
    // docid.onmouseup() = getText;
}
console.log("document:" + document);
window.onload = testcase;
