from flask import Flask, render_template, request

app = Flask(__name__)
FILE = "contacts.txt"

def load_contacts():
    contacts = {}
    try:
        with open(FILE, "r") as f:
            for line in f:
                line = line.strip()
                if ":" in line:
                    name, number = line.split(":")
                    contacts[name] = number
    except FileNotFoundError:
        open(FILE, "w").close()
    return contacts


def save_contacts(contacts):
    with open(FILE, "w") as f:
        for name, number in contacts.items():
            f.write(f"{name}:{number}\n")


@app.route("/", methods=["GET", "POST"])
def home():
    contacts = load_contacts()
    message = ""

    if request.method == "POST":
        action = request.form.get("action")
        name = request.form.get("name")
        number = request.form.get("number")

        
        if action == "add":
            if name and number:
                contacts[name] = number
                save_contacts(contacts)
                message = "Contact added successfully!"
            else:
                message = "Please enter both name and number."

        
        elif action == "search":
            if name in contacts:
                message = f"{name} → {contacts[name]}"
            else:
                message = "Contact not found!"

       
        elif action == "delete":
            if name in contacts:
                del contacts[name]
                save_contacts(contacts)
                message = "Contact deleted!"
            else:
                message = "This contact does not exist!"

    return render_template("index.html", contact=contacts, message=message)


if __name__ == "__main__":
    app.run(debug=True)

