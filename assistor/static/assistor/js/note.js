document.addEventListener("DOMContentLoaded", () => {
    document.querySelector("#addNoteButton").onclick = addNote;
    document.querySelector("#editNoteButton").onclick = editNote;
});

function addNote() {
    const request = new XMLHttpRequest();
    const form = document.forms['newNoteForm'];
    const courseId = document.querySelector("#course_id").value;
    var formData = new FormData(form);
    var originalText;

    
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
        let jsonResponse = JSON.parse(this.responseText)

        // Display the course
        if (this.status == 201) {
            window.location = "/courses/" + jsonResponse.course + "/notes/" + jsonResponse.id;
        }

        // Show the errors on forms
        else if (this.status == 400) {
            renderFormErrors(form, jsonResponse);
        }
    }
    request.open("POST", "/courses/" + courseId + "/notes/new");
    request.send(formData);
}

function editNote() {
    const request = new XMLHttpRequest();
    const form = document.forms['editNoteForm'];
    const courseId = document.querySelector("#course_id").value;
    const noteId = document.querySelector("#note_id").value;
    var formData = new FormData(form);
    var originalText;

    
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
        let jsonResponse = JSON.parse(this.responseText)

        // Display the course
        if (this.status == 201) {
            window.location = "/courses/" + jsonResponse.course + "/notes/" + jsonResponse.id;
        }

        // Show the errors on forms
        else if (this.status == 400) {
            renderFormErrors(form, jsonResponse);
        }
    }
    request.open("POST", "/courses/" + courseId + "/notes/" + noteId + "/edit");
    request.send(formData);
}

