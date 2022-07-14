document.addEventListener("DOMContentLoaded", () => {
    document.querySelector("#addLinkButton").onclick = addLink;
});

function addLink() {
    const request = new XMLHttpRequest();
    const form = document.forms['newLinkForm'];
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
        

        // Display the link
        if (this.status == 201) {
            window.location = "/courses/" + jsonResponse.course;
        }

        // Show the errors on forms
        else if (this.status == 400) {
            renderFormErrors(form, jsonResponse);
        }
    }
    request.open("POST", "/courses/" + courseId + "/links/new");
    request.send(formData);
}

