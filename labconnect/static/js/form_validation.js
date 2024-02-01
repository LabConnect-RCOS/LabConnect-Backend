function validateForm() {
  var nameField = document.getElementById("name");
  var descriptionField = document.getElementById("description");
  var compensationField = document.getElementById("compensation");
  var emailField = document.getElementById("email");
  var applicationDueField = document.getElementById("application_due");

  if (nameField.value.trim() == "") {
    alert("Job Title is required.");
    nameField.focus();
    return false;
  }

  if (descriptionField.value.trim() == "") {
    alert("Job Description is required.");
    descriptionField.focus();
    return false;
  }

  if (compensationField.value == "Select") {
    alert("Mode of Compensation is required.");
    compensationField.focus();
    return false;
  }

  var email = emailField.value;
  var emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
  if (!emailPattern.test(email)) {
    alert("Please enter a valid email address.");
    emailField.focus();
    return false;
  }

  var applicationDueValue = applicationDueField.value;
  var datePattern = /^(0[1-9]|1[0-2])\/(0[1-9]|[12][0-9]|3[01])\/\d{4}$/;
  var currentDate = new Date();
  var enteredDate = new Date(applicationDueValue);

  if (applicationDueField.value == "") {
    alert("Application Due Date is required.");
    applicationDueField.focus();
    return false;
  } else if (!datePattern.test(applicationDueValue)) {
    alert("Please enter a valid date in the format MM/DD/YYYY.");
    applicationDueField.focus();
    return false;
  } else if (enteredDate <= currentDate) {
    alert("Application Due Date must be in the future.");
    applicationDueField.focus();
    return false;
  }

  return true;
}
