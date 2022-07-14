document.addEventListener("DOMContentLoaded", () => {
    document.querySelector("#addFileButton").onclick = addFile;
    document.querySelector("#editFileButton").onclick = editFile;
});

function addFile() {
    const request = new XMLHttpRequest();
    const form = document.forms['newFileForm'];
    const courseId = document.querySelector("#course_id").value;
    var formData = new FormData(form);
    var originalText;

    // Show loading spinner
    request.onloadstart = () => {
        originalText = this.innerHTML;
        this.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>';
    }

    // Stop loading spinner
    request.onloadend = () => {
        this.innerHTML = originalText;
    }

    request.onload = function() {
        let jsonResponse = JSON.parse(this.responseText);

        // Display the file
        if (this.status == 201) {
            window.location = "/courses/" + jsonResponse.course + "/files/" + jsonResponse.id;
        }

        // Show the errors on forms
        else if (this.status == 400) {
            renderFormErrors(form, jsonResponse);
        }
    }
    request.open("POST", "/courses/" + courseId + "/files/new");
    request.send(formData);
}

function editFile() {
    const request = new XMLHttpRequest();
    const form = document.forms['editFileForm'];
    const courseId = document.querySelector("#course_id").value;
    const fileId = document.querySelector("#file_id").value;
    var formData = new FormData(form);
    
    var originalText;

    // Show loading spinner
    request.onloadstart = () => {
        originalText = this.innerHTML;
        this.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>';
    }

    // Stop loading spinner
    request.onloadend = () => {
        this.innerHTML = originalText;
    }

    request.onload = function() {
        let jsonResponse = JSON.parse(this.responseText);

        // Display the file
        if (this.status == 201) {
            window.location = "/courses/" + jsonResponse.course + "/files/" + jsonResponse.id;
        }

        // Show the errors on forms
        else if (this.status == 400) {
            renderFormErrors(form, jsonResponse);
        }
    }
    request.open("POST", "/courses/" + courseId + "/files/" + fileId + "/edit");
    request.send(formData);
}

