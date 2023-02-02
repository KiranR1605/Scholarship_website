from Student_Scholarship_Portal import app, db
from flask import render_template, redirect, url_for, request, flash, send_file
from Student_Scholarship_Portal.models import User, Applicant, Bank, Current_education, Education,Scholarship , Queries
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from io import BytesIO
from flask_mail import Mail, Message
import smtplib


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = ''
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)


@app.route("/")
@app.route('/home')
def home_page():
    return render_template('home.html', user = current_user)


@app.route("/login", methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                if user.admin_access == False:
                    login_user(user, remember = True)
                    return redirect(url_for('scholarship_page'))
                else:
                    login_user(user, remember = True)
                    return redirect(url_for('add_page'))
            else:
                flash('Incorrect Password!', category='danger')
        else:
            flash('No User with the Email exists!', category='danger')

    return render_template('login.html', user = current_user)


@app.route("/logout")
@login_required
def logout_page():
    logout_user()
    return redirect(url_for('home_page'))


@app.route("/register", methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        password1 = request.form.get('password')
        password2 = request.form.get('confirm-password')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Account with the Email as already been created!',
                  category='danger')
        elif len(email) < 4 or len(email) > 50:
            flash('Email must be between 3 to 50 characters.', category='danger')
        elif len(name) < 2 or len(name) > 30:
            flash('Name must be between 2 to 30 characters.', category='danger')
        elif len(phone) != 10:
            flash('Enter a valid Contact Number!', category='danger')
        elif len(password1) < 8:
            flash('Password must be atleast than 7 characters.', category='danger')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='danger')
        else:
            new_user = User(name=name,
                            phone=phone,
                            email=email,
                            password=generate_password_hash(password1, method="sha256"))
            db.session.add(new_user)
            db.session.commit()

            with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
                connection.starttls()
                connection.login(
                    user='', password='')
                connection.sendmail(
                    from_addr='',
                    to_addrs=f'{email}',
                    msg=f"Subject: Conformation Mail\n\n THANK YOU FOR REGISTERING TO SCHOLARSHIP PORTAL!! \n\n THESE ARE YOUR LOGIN CREDENTIALS \n Name: {name} \n Phone no.: {phone} \n Email: {email} \n Password: {password1} "
                )
            connection.close()

            flash('Account created successfully!', category='success')
            login_user(user, remember = True)
            return redirect(url_for('scholarship_page'))

    return render_template('register.html', user = current_user)


@app.route("/contact", methods=['GET', 'POST'])
def contact_page():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')

        query = Queries(name=name,
                        email=email,
                        subject=subject,
                        message=message)
        db.session.add(query)
        db.session.commit()

        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(
                user='', password='')
            connection.sendmail(
                from_addr='',
                to_addrs=f'',
                msg=f"Subject: USER QUERY - {subject}\n\n Name: {name} \n Email: {email} \n Message: {message} "
            )
        connection.close()

        flash('Your Query has been received we will reach you with a solution soon.', category = 'success')
        return redirect(url_for('home_page'))

    return render_template('contact.html', user = current_user)


@app.route("/about")
def about_page():
    return render_template('about.html', user = current_user)


@app.route("/principal")
def principal_page():
    return render_template('principal.html', user = current_user)


@app.route("/vice")
def vice_page():
    return render_template('vice.html', user = current_user)


@app.route("/qa")
def QA_page():
    return render_template('qa.html', user = current_user)


@app.route("/dashboard", methods=['GET', 'POST'])
@login_required
def scholarship_page():
    scholarships = Scholarship.query.all()
    return render_template('scholarship.html', scholarships=scholarships, user = current_user)


@app.route("/detail/<s_id>")
@login_required
def detail_page(s_id):
    scholarship = Scholarship.query.filter_by(id = s_id).first()
    return render_template('detail.html', scholarship = scholarship, user = current_user)


@app.route("/faq")
@login_required
def faq_page():
    return render_template('faq.html', user = current_user)


@app.route("/add", methods = ['GET', 'POST'])
@login_required
def add_page():
    if request.method == 'POST':
        sName = request.form.get('sName')
        abt_programme = request.form.get('abt_programme')
        eligibility = request.form.get('eligibility')
        documents_required = request.form.get('documents_required')
        benefits = request.form.get('benefits')
        deadline = request.form.get('deadline')

        scholarship = Scholarship(sName = sName,
                                  abt_programme = abt_programme,
                                  eligibility = eligibility,
                                  documents_required = documents_required,
                                  benefits = benefits,
                                  deadline = deadline)
        db.session.add(scholarship)
        db.session.commit()

        flash('Scholarship has been added successfully.', category = 'success')
        return redirect(url_for('add_page'))

    return render_template('add.html', user = current_user)


@app.route("/view")
@login_required
def view_page():
    scholarships = Scholarship.query.all()
    return render_template('view.html', scholarships = scholarships, user = current_user)


@app.route("/student")
@login_required
def student_page():
    applicants = Applicant.query.all()
    scholarships = Scholarship.query.all()
    return render_template('student.html', applicants = applicants ,scholarships = scholarships ,user = current_user)


@app.route("/form/<s_id>", methods = ['GET', 'POST'])
@login_required
def applicant_form_page(s_id):
    if request.method == 'POST':
        identity_proof = request.files['identity_proof']
        income_certificate = request.files['income_certificate']
        address_proof = request.files['address_proof']
        passbook = request.files['passbook']
        fee_receipt = request.files['fee_receipt']
        admission_letter = request.files['admission_letter']
        marksheet10 = request.files['marksheet10']
        marksheet12 = request.files['marksheet12']

        bank = Bank(accNo = request.form.get('accNo'),
                    IFSC = request.form.get('IFSC'),
                    bName = request.form.get('bName'),
                    branch = request.form.get('branch'),
                    accName = request.form.get('accName'),
                    passbook_filename = passbook.filename,
                    passbook_data = passbook.read())
        
        db.session.add(bank)
        db.session.flush()
        bank_id = bank.id

        current_education = Current_education(cLevel = request.form.get('cLevel'),
                                              cName = request.form.get('cName'),
                                              clgName = request.form.get('clgName'),
                                              cState = request.form.get('cState'),
                                              tFee = request.form.get('tFee'),
                                              ntFee = request.form.get('ntFee'),
                                              fee_receipt_filename = fee_receipt.filename,
                                              fee_receipt_data = fee_receipt.read(),
                                              admission_letter_filename = admission_letter.filename,
                                              admission_letter_data = admission_letter.read())

        db.session.add(current_education)
        db.session.flush()
        current_education_id = current_education.id

        education = Education(name10 = request.form.get('name10'),
                              state10 = request.form.get('state10'),
                              pass10 = request.form.get('pass10'),
                              per10 = request.form.get('per10'),
                              marksheet10_filename = marksheet10.filename,
                              marksheet10_data = marksheet10.read(),
                              name12 = request.form.get('name12'),
                              state12 = request.form.get('state12'),
                              pass12 = request.form.get('pass12'),
                              per12 = request.form.get('per12'),
                              marksheet12_filename = marksheet12.filename,
                              marksheet12_data = marksheet12.read())

        db.session.add(education)
        db.session.flush()
        education_id = education.id

        applicant = Applicant(name = request.form.get('name'),
                              DOB = request.form.get('DOB'),
                              gender = request.form.get('gender'),
                              category = request.form.get('category'),
                              USN = request.form.get('USN'),
                              email = request.form.get('email'),
                              phone = request.form.get('phone'),
                              income = request.form.get('income'),
                              identity_proof_filename = identity_proof.filename,
                              identity_proof_data = identity_proof.read(),
                              income_certificate_filename = income_certificate.filename,
                              income_certificate_data = income_certificate.read(),
                              address = request.form.get('address'),
                              pin = request.form.get('pin'),
                              area = request.form.get('area'),
                              district = request.form.get('district'),
                              state = request.form.get('state'),
                              address_proof_filename = address_proof.filename,
                              address_proof_data = address_proof.read(),
                              user_id = current_user.id,
                              bank_id = bank_id,
                              current_education_id = current_education_id,
                              education_id = education_id,
                              scholarship_id = s_id)
        
        db.session.add(applicant)
        db.session.commit()

        flash('Your application has been successfully submitted.', category = 'success')
        return redirect(url_for('scholarship_page'))

    return render_template('applicant-form.html', user = current_user, s_id = s_id)


@app.route("/application/<a_id>", methods = ['GET', 'POST'])
@login_required
def application(a_id):
    applicant = Applicant.query.filter_by(id = a_id).first()
    bank = Bank.query.filter_by(id = applicant.bank_id).first()
    education = Education.query.filter_by(id = applicant.education_id).first()
    Ceducation = Current_education.query.filter_by(id = applicant.current_education_id).first()

    if request.method== 'POST':
        document_requested = request.form.get('btn')

        match document_requested:
            case 'identity':
                return send_file(BytesIO(applicant.identity_proof_data), as_attachment = True, download_name = applicant.identity_proof_filename)

            case 'income':
                return send_file(BytesIO(applicant.income_certificate_data), as_attachment = True, download_name = applicant.income_certificate_filename)

            case 'address':
                return send_file(BytesIO(applicant.address_proof_data), as_attachment = True, download_name = applicant.address_proof_filename)

            case 'passbook':
                return send_file(BytesIO(bank.passbook_data), as_attachment = True, download_name = bank.passbook_filename)

            case 'class10':
                return send_file(BytesIO(education.marksheet10_data), as_attachment = True, download_name = education.marksheet10_filename)

            case 'class12':
                return send_file(BytesIO(education.marksheet12_data), as_attachment = True, download_name = education.marksheet12_filename)

            case 'fee':
                return send_file(BytesIO(Ceducation.fee_receipt_data), as_attachment = True, download_name = Ceducation.fee_receipt_filename)
                
            case 'admission':
                return send_file(BytesIO(Ceducation.admission_letter_data), as_attachment = True, download_name = Ceducation.admission_letter_filename)

        return redirect(url_for('application', a_id = a_id))

    return render_template('application.html', user = current_user, applicant = applicant, bank = bank, education = education, Ceducation = Ceducation)


@app.route('/delete_s/<s_id>')
@login_required
def delete_scholarship(s_id):
    scholarship = Scholarship.query.filter_by(id = s_id).first()
    db.session.delete(scholarship)
    db.session.commit()
        
    return redirect(url_for('view_page'))
    
@app.route('/delete_a/<a_id>')
@login_required
def delete_application(a_id):
    applicant = Applicant.query.filter_by(id = a_id).first()
    bank = Bank.query.filter_by(id = applicant.bank_id).first()
    education = Education.query.filter_by(id = applicant.education_id).first()
    Ceducation = Current_education.query.filter_by(id = applicant.current_education_id).first()
    
    db.session.delete(applicant)
    db.session.delete(bank)
    db.session.delete(education)
    db.session.delete(Ceducation)
    db.session.commit()
        
    return redirect(url_for('student_page'))

@app.route('/list/<s_id>')
@login_required
def scholarship_list_page(s_id):
    applicants = Applicant.query.filter_by(scholarship_id = s_id).all()
    scholarship = Scholarship.query.filter_by(id = s_id).first()
    return render_template('list.html', user = current_user, applicants = applicants, scholarship = scholarship)