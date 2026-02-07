from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Simple knowledge base
knowledge_base = {
    "fees": "The total fees are ₹50,000 per semester.",
    "exam": "The semester exams will start from 10th March.",
    "timetable": "The timetable is available on the university website.",
    "scholarship": "Scholarship applications open in July every year.",
    "admission": "Admissions are open from June to August."
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message").lower()

    for keyword in knowledge_base:
        if keyword in user_message:
            return jsonify({"reply": knowledge_base[keyword]})

    return jsonify({"reply": "I am not sure about this. Please contact the admin."})

if __name__ == "__main__":
    app.run(debug=True)