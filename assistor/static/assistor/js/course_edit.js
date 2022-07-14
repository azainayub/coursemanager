document.addEventListener("DOMContentLoaded", () => {
    document.querySelector("#editCourseButton").onclick = editCourse;
});

function editCourse() {
    const request = new XMLHttpRequest();
    const form = document.forms['editCourseForm'];
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
            window.location = "/courses/" + jsonResponse.id;
        }

        // Show the errors on forms
        else if (this.status == 400) {
            renderFormErrors(form, jsonResponse);
        }
    }
    request.open("POST", "/courses/" + courseId + "/edit");
    request.send(formData);
}