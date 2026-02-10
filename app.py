from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)

# ---------- CONFIG ----------
app.secret_key = "secret123"

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"


# ---------- HOME PAGE ----------
@app.route("/")
def index():
    conn = sqlite3.connect("services.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM services")
    services = cursor.fetchall()
    conn.close()
    return render_template("index.html", services=services)


# ---------- BOOK SERVICE ----------
@app.route("/book/<service_name>")
def book(service_name):
    return render_template("book.html", service_name=service_name)


# ---------- SUBMIT BOOKING ----------
@app.route("/submit_booking", methods=["POST"])
def submit_booking():
    name = request.form["name"]
    service = request.form["service"]
    date = request.form["date"]

    conn = sqlite3.connect("services.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO bookings (customer_name, service_name, booking_date) VALUES (?, ?, ?)",
        (name, service, date)
    )
    conn.commit()
    conn.close()

    return redirect("/bookings")


# ---------- USER BOOKINGS ----------
@app.route("/bookings")
def bookings():
    conn = sqlite3.connect("services.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bookings")
    bookings = cursor.fetchall()
    conn.close()
    return render_template("my_bookings.html", bookings=bookings)


# ---------- ADMIN LOGIN ----------
@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect("/admin")
        else:
            error = "Invalid credentials"

    return render_template("admin_login.html", error=error)


# ---------- ADMIN PANEL ----------
@app.route("/admin")
def admin():
    if not session.get("admin"):
        return redirect("/admin-login")

    conn = sqlite3.connect("services.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bookings")
    bookings = cursor.fetchall()
    conn.close()
    return render_template("admin.html", bookings=bookings)


# ---------- UPDATE STATUS ----------
@app.route("/update_status/<int:booking_id>")
def update_status(booking_id):
    if not session.get("admin"):
        return redirect("/admin-login")

    conn = sqlite3.connect("services.db")
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE bookings SET status=? WHERE id=?",
        ("Completed", booking_id)
    )
    conn.commit()
    conn.close()

    return redirect("/admin")


# ---------- LOGOUT ----------
@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect("/")


# ---------- RUN ----------
if __name__ == "__main__":
    app.run(debug=True)

