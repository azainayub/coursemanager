function renderFormErrors(form, fields) {
    // The div element inside form where errors will rendered
    const errorsElement = document.getElementById("errors");

    // List of fields
    let fieldsList = document.createElement("ul");
    for (let field in fields) {
        let fieldItem = document.createElement("li");
        fieldItem.innerHTML = field;
        let errorList = document.createElement("ol");
        
        for (let error of fields[field]) {
            let errorItem = document.createElement("li");
            errorItem.innerHTML = error;
            errorItem.className = "text-danger";
            errorList.appendChild(errorItem);
        }

        fieldItem.appendChild(errorList);
        fieldsList.appendChild(fieldItem);
    }

    errorsElement.innerHTML = "";
    errorsElement.appendChild(fieldsList);
}
