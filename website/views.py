from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import User, Patient, Caregiver, Appointment, Assignment
from . import db
from datetime import datetime

views = Blueprint('views', __name__)

# Route to add a patient
@views.route('/add_patient', methods=['GET', 'POST'])
@login_required
def add_patient():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        medical_records = request.form['medical_records']
        
        new_patient = Patient(name=name, address=address, medical_records=medical_records)
        db.session.add(new_patient)
        db.session.commit()
        flash('Patient added successfully!', 'success')
        return redirect(url_for('views.manage_patients'))
    
    return render_template('add_patient.html')

# Route to manage patients
@views.route('/manage_patients', methods=['GET'])
@login_required
def manage_patients():
    patients = Patient.query.all()
    return render_template('manage_patients.html', patients=patients)

@views.route('/delete_patient/<int:patient_id>', methods=['GET'])
@login_required
def delete_patient(patient_id):
    patient = Patient.query.get(patient_id)
    if patient:
        # Delete all associated appointments first
        Appointment.query.filter_by(patient_id=patient.id).delete()
        
        # Now delete the patient
        db.session.delete(patient)
        db.session.commit()
        flash('Patient and all related appointments deleted successfully!', 'success')
    else:
        flash('Patient not found!', 'danger')
    return redirect(url_for('views.manage_patients'))


# Route to assign a caregiver to a patient
@views.route('/assign_caregiver', methods=['GET', 'POST'])
@login_required
def assign_caregiver():
    if request.method == 'POST':
        caregiver_id = request.form['caregiver_id']
        patient_id = request.form['patient_id']

        new_assignment = Assignment(caregiver_id=caregiver_id, patient_id=patient_id)
        db.session.add(new_assignment)
        db.session.commit()
        flash('Caregiver assigned successfully!', 'success')
        return redirect(url_for('views.manage_assignments'))

    caregivers = Caregiver.query.all()
    patients = Patient.query.all()
    return render_template('assign_caregiver.html', caregivers=caregivers, patients=patients)

# Route to manage caregiver assignments
@views.route('/manage_assignments', methods=['GET'])
@login_required
def manage_assignments():
    assignments = db.session.query(Assignment, Caregiver, Patient).join(Caregiver, Assignment.caregiver_id == Caregiver.id).join(Patient, Assignment.patient_id == Patient.id).all()
    return render_template('manage_assignments.html', assignments=assignments)


# Route to remove a caregiver assignment
@views.route('/remove_assignment/<int:assignment_id>', methods=['GET'])
@login_required
def remove_assignment(assignment_id):
    assignment = Assignment.query.get(assignment_id)
    if assignment:
        db.session.delete(assignment)
        db.session.commit()
        flash('Assignment removed successfully!', 'success')
    else:
        flash('Assignment not found!', 'danger')
    return redirect(url_for('views.manage_assignments'))

# Route to schedule an appointment
@views.route('/schedule_appointments', methods=['GET', 'POST'])
@login_required
def schedule_appointments():
    if request.method == 'POST':
        caregiver_id = request.form['caregiver_id']
        patient_id = request.form['patient_id']
        date_str = request.form['date']  # Get the date as a string

        # Convert the date string into a datetime object
        try:
            # Assume the date is in 'YYYY-MM-DD' format
            appointment_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid date format. Please use YYYY-MM-DD.', 'danger')
            return redirect(url_for('views.schedule_appointments'))

        # Create a new appointment instance
        new_appointment = Appointment(caregiver_id=caregiver_id, patient_id=patient_id, date=appointment_date)
        
        try:
            # Add the new appointment to the database
            db.session.add(new_appointment)
            db.session.commit()
            flash('Appointment scheduled successfully!', 'success')
            return redirect(url_for('views.view_appointments'))
        except Exception as e:
            db.session.rollback()  # Rollback in case of error
            flash('Error occurred while scheduling appointment: ' + str(e), 'danger')
            return redirect(url_for('views.schedule_appointments'))

    # Render the schedule appointments form
    caregivers = Caregiver.query.all()
    patients = Patient.query.all()
    return render_template('schedule_appointments.html', caregivers=caregivers, patients=patients)
# Route to view appointments
@views.route('/view_appointments', methods=['GET'])
@login_required
def view_appointments():
    appointments = db.session.query(Appointment, Caregiver, Patient).join(Caregiver, Appointment.caregiver_id == Caregiver.id).join(Patient, Appointment.patient_id == Patient.id).all()
    return render_template('view_appointments.html', appointments=appointments)


# Route to update an appointment
@views.route('/update_appointment/<int:appointment_id>', methods=['GET', 'POST'])
@login_required
def update_appointment(appointment_id):
    appointment = Appointment.query.get(appointment_id)
    if request.method == 'POST':
        if appointment:
            appointment.caregiver_id = request.form['caregiver_id']
            appointment.patient_id = request.form['patient_id']
            appointment.date = request.form['date']
            db.session.commit()
            flash('Appointment updated successfully!', 'success')
            return redirect(url_for('views.view_appointments'))
        else:
            flash('Appointment not found!', 'danger')
    
    caregivers = Caregiver.query.all()
    patients = Patient.query.all()
    return render_template('update_appointment.html', appointment=appointment, caregivers=caregivers, patients=patients)

# Route to delete an appointment
@views.route('/delete_appointment/<int:appointment_id>', methods=['GET'])
@login_required
def delete_appointment(appointment_id):
    appointment = Appointment.query.get(appointment_id)
    if appointment:
        db.session.delete(appointment)
        db.session.commit()
        flash('Appointment deleted successfully!', 'success')
    else:
        flash('Appointment not found!', 'danger')
    return redirect(url_for('views.view_appointments'))

# Route to add a caregiver
@views.route('/add_caregiver', methods=['GET', 'POST'])
@login_required
def add_caregiver():
    if request.method == 'POST':
        # Retrieve form data
        name = request.form.get('name')
        contact_info = request.form.get('contact_info')
        
        # Ensure the fields are not empty
        if not name or not contact_info:
            flash('Please fill in all the fields.', 'danger')
            return redirect(url_for('views.add_caregiver'))
        
        # Create a new caregiver instance and add it to the database
        new_caregiver = Caregiver(name=name, contact_info=contact_info)
        
        try:
            # Add the new caregiver to the database
            db.session.add(new_caregiver)
            db.session.commit()
            flash('Caregiver added successfully!', 'success')
            return redirect(url_for('views.add_caregiver'))
        except Exception as e:
            db.session.rollback()  # Rollback in case of error
            flash('Error occurred while adding caregiver: ' + str(e), 'danger')
            return redirect(url_for('views.add_caregiver'))
    
    # Render the add caregiver form
    return render_template('add_caregiver.html')

# Route to main options page
@views.route('/')
@views.route('/main_options')
@login_required
def main_options():
    return render_template('main_options.html')
