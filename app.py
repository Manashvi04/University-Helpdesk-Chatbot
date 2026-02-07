from flask import Flask, render_template, request, jsonify
from db import get_connection

app = Flask(__name__)

rules = {

    # 🔹 FEES & PAYMENTS
    "fees": "Fees can be paid online through the university portal or at the accounts office.",
    "fee payment": "You can pay fees using net banking, debit card, or UPI via the university portal.",
    "late fee": "Late fee payment may attract a penalty. Please check the academic calendar.",
    "refund": "Fee refund is applicable as per university refund policy available on the website.",

    # 🔹 EXAMS
    "exam": "Exam schedule is available on the university website under the examination section.",
    "exam date": "Exam dates are announced on the official exam portal.",
    "hall ticket": "Hall tickets can be downloaded from the exam portal one week before exams.",
    "revaluation": "Students can apply for revaluation through the exam cell within the given deadline.",
    "backlog": "Backlog exams are conducted during supplementary examination sessions.",

    # 🔹 TIMETABLE & CLASSES
    "timetable": "The class timetable is updated every semester on the student portal.",
    "class schedule": "Class schedules are shared by the department and uploaded on the portal.",
    "online class": "Online class links are shared via LMS or official email.",
    "attendance": "Minimum 75% attendance is required to appear for exams.",

    # 🔹 SCHOLARSHIPS
    "scholarship": "Scholarships are provided based on merit, income, and government norms.",
    "scholarship form": "Scholarship forms are available on the government scholarship portal.",
    "scholarship status": "You can check scholarship status on the official scholarship website.",
    "renewal": "Scholarship renewal must be done every academic year.",

    # 🔹 ADMISSIONS
    "admission": "Admission details are available on the university admission portal.",
    "eligibility": "Eligibility criteria differ for each course and are mentioned in the prospectus.",
    "documents": "Required documents include marksheets, ID proof, and transfer certificate.",
    "admission status": "Admission status can be checked using your application number.",

    # 🔹 RESULTS
    "result": "Results are published on the university website after evaluation.",
    "marksheet": "Mark sheets can be downloaded from the student portal.",
    "grade": "Grades are awarded based on university evaluation guidelines.",
    "cgpa": "CGPA is calculated as per the university grading system.",

    # 🔹 CERTIFICATES
    "bonafide": "Bonafide certificates can be requested through the student portal.",
    "tc": "Transfer Certificate can be applied for after course completion.",
    "migration": "Migration certificate requests are handled by the exam section.",
    "degree certificate": "Degree certificates are issued during convocation.",

    # 🔹 HOSTEL
    "hostel": "Hostel admission details are available on the hostel office notice board.",
    "hostel fees": "Hostel fees must be paid separately through the hostel portal.",
    "room allotment": "Room allotment is done based on availability and merit.",
    "mess": "Mess menu and timings are displayed in the hostel premises.",

    # 🔹 LIBRARY
    "library": "The university library is open from 9 AM to 8 PM.",
    "library card": "Library cards are issued by the library office.",
    "book issue": "Books can be issued using your library card.",
    "fine": "Late return of books attracts a fine as per library rules.",

    # 🔹 PLACEMENTS
    "placement": "Placement activities are managed by the placement cell.",
    "internship": "Internship opportunities are shared through the placement portal.",
    "company": "Company visit details are shared via email and notice boards.",
    "resume": "Resume guidelines are provided by the placement cell.",

    # 🔹 ID & LOGIN
    "id card": "ID cards are issued by the administration office.",
    "lost id": "Lost ID cards can be reissued after submitting an application.",
    "portal login": "Portal login issues can be resolved by the IT helpdesk.",

    # 🔹 GENERAL
    "holiday": "Holiday list is available on the university academic calendar.",
    "calendar": "Academic calendar is published on the university website.",
    "contact": "You can contact the university office during working hours.",
    "office timing": "Office timing is from 10 AM to 5 PM on working days."
}


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_msg = data.get("message", "").lower()

    reply = "Sorry, I will forward this to human support."

    for key in rules:
        if key in user_msg:
            reply = rules[key]
            break

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO chats (user_message, bot_reply) VALUES (?, ?)",
        user_msg, reply
    )

    if reply.startswith("Sorry"):
        cursor.execute(
            "INSERT INTO unanswered (question) VALUES (?)",
            user_msg
        )

    conn.commit()
    conn.close()

    return jsonify({"reply": reply})

@app.route("/admin")
def admin():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM unanswered")
    questions = cursor.fetchall()
    conn.close()
    return render_template("admin.html", questions=questions)

if __name__ == "__main__":
    app.run(debug=True)
