'''
Enunciado

Crie uma API Flask para gerenciar tarefas (todos) em memória.

Endpoints

POST /tasks

GET /tasks

GET /tasks/<id>

Estrutura de uma tarefa
{
  "title": "Estudar Python",
  "done": false
}
'''


from flask import Flask, request, jsonify, abort

app = Flask(__name__)

tasks = []
next_id = 1


@app.route("/tasks", methods=["POST"])
def create_task():
    global next_id

    data = request.get_json()
    if not data or "title" not in data:
        abort(400, "title is required")

    task = {
        "id": next_id,
        "title": data["title"],
        "done": data.get("done", False),
    }

    tasks.append(task)
    next_id += 1

    return jsonify(task), 201


@app.route("/tasks", methods=["GET"])
def list_tasks():
    return jsonify(tasks)


@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            return jsonify(task)

    abort(404, "task not found")


if __name__ == "__main__":
    app.run(debug=True)
