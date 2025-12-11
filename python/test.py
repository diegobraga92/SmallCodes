from flask import Flask, request, abort, jsonify

class User:
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email

    def to_dict(self):
        return {"id": f"{self.id}", "name": f"{self.name}", "email": f"{self.email}"}

DB = {
    1: User(1, "D", "D@D"),
    2: User(2, "B", "B@B")
}

NEXT_ID = 2

app = Flask(__name__)

@app.route("/users", methods=["POST"])
def create_user():
    if not request.is_json:
        abort(419, "Payload missing")

    data = request.get_json()
    name = data.get("name")
    email = data.get("email")

    global NEXT_ID
    NEXT_ID += 1

    user = User(NEXT_ID, name, email)
    DB[NEXT_ID] = user

    return jsonify(user.to_dict())

@app.route("/users", methods=["GET"])
def get_users():
    name = request.args.get("name")

    if name:
        return [x.to_dict() for x in DB.values() if name in x.name]    

    return [x.to_dict() for x in DB.values()]

@app.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    return jsonify(DB[id].to_dict())


if __name__ == "__main__":
    app.run("0.0.0.0", 5000)






