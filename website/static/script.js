// scripts.js

document.addEventListener('DOMContentLoaded', function () {
    console.log("Welcome to JKL Healthcare Services!");

    // Helper function to show confirmation dialog
    function confirmDelete(event) {
        if (!confirm("Are you sure you want to delete this item? This action cannot be undone.")) {
            event.preventDefault();
        }
    }

    // Confirm delete action for all delete buttons
    document.querySelectorAll('.btn-danger').forEach(button => {
        button.addEventListener('click', confirmDelete);
    });

    // Form validation helper functions
    function validatePasswords(password1, password2) {
        if (password1 !== password2) {
            alert("Passwords do not match!");
            return false;
        }
        return true;
    }

    function validateNotEmpty(inputs) {
        for (const input of inputs) {
            if (input.value.trim() === "") {
                alert("Please fill in all required fields!");
                return false;
            }
        }
        return true;
    }

    function validateFutureDate(dateInput) {
        const selectedDate = new Date(dateInput.value);
        const currentDate = new Date();
        if (selectedDate < currentDate) {
            alert("Please select a valid date that is not in the past.");
            return false;
        }
        return true;
    }

    // User Registration Form Handling
    const registerForm = document.querySelector('form[action="{{ url_for("auth.sign_up") }}"]');
    if (registerForm) {
        registerForm.addEventListener('submit', function (event) {
            const password1 = document.getElementById('password1').value;
            const password2 = document.getElementById('password2').value;
            if (!validatePasswords(password1, password2)) {
                event.preventDefault();
            }
        });
    }

    // Patient Management: Add Patient Form
    const addPatientForm = document.querySelector('form[action="{{ url_for("views.add_patient") }}"]');
    if (addPatientForm) {
        addPatientForm.addEventListener('submit', function (event) {
            const requiredFields = [document.getElementById('name'), document.getElementById('address')];
            if (!validateNotEmpty(requiredFields)) {
                event.preventDefault();
            }
        });
    }

    // Caregiver Assignment: Assign Caregiver Form
    const assignCaregiverForm = document.querySelector('form[action="{{ url_for("views.assign_caregiver") }}"]');
    if (assignCaregiverForm) {
        assignCaregiverForm.addEventListener('submit', function (event) {
            const caregiverId = document.getElementById('caregiver_id').value;
            const patientId = document.getElementById('patient_id').value;
            if (!validateNotEmpty([caregiverId, patientId])) {
                alert("Please select both a caregiver and a patient!");
                event.preventDefault();
            }
        });
    }

    // Appointment Scheduling: Validate date selection
    const scheduleForm = document.querySelector('form[action="{{ url_for("views.schedule_appointments") }}"]');
    if (scheduleForm) {
        scheduleForm.addEventListener('submit', function (event) {
            const dateInput = document.getElementById('date');
            if (!validateFutureDate(dateInput)) {
                event.preventDefault();
            }
        });
    }

    // Dropdown selection logging for caregivers and patients
    document.getElementById('caregiver_id')?.addEventListener('change', function () {
        console.log(`Selected Caregiver: ${this.value}`);
    });
    document.getElementById('patient_id')?.addEventListener('change', function () {
        console.log(`Selected Patient: ${this.value}`);
    });

    // Appointment Update Form Handling
    document.querySelectorAll('form[action="{{ url_for("views.update_appointment") }}"]').forEach(form => {
        form.addEventListener('submit', function (event) {
            const dateInput = document.getElementById('date');
            if (!validateFutureDate(dateInput)) {
                event.preventDefault();
            }
        });
    });

    // Hide feedback message after 5 seconds
    const feedback = document.getElementById('feedback');
    if (feedback) {
        setTimeout(() => {
            feedback.style.display = 'none';
        }, 5000);
    }
});
