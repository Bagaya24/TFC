from flask import Flask, request, render_template, redirect, Response
import ollama

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')


@app.route("/prompt", methods=["POST"])
def prompt():
    messages = request.json["messages"]
    conversation = construction_conversation(messages)

    return Response(assistant(conversation), mimetype="text/event-stream")


@app.route("/alimentaire")
def alimentaire():
    return render_template("page_tableau_alimentaire.html")


@app.route("/boisson")
def boisson():
    return render_template("page_tableau_boisson.html")


@app.route("/cosmetique")
def cosmetique():
    return render_template("page_tableau_cosmetique.html")


@app.route("/eletromenage")
def electromenage():
    return render_template("page_tableau_eletromenage.html")


@app.route("/utilisateur")
def utilisateur():
    return render_template("page_utilisateur.html")

def construction_conversation(message: list) -> list[dict]:
    return [
        {"role": "user" if i % 2 == 0 else "assistant", "content": message}
        for i, message in enumerate(message)
    ]


def assistant(conversation: list[dict]) -> str:
    reponse_assistant = ollama.chat(model="assistant_1",
                                    messages=conversation,
                                    )
    print(reponse_assistant["message"]["content"])
    yield reponse_assistant["message"]["content"]


if __name__ == "__main__":
    app.run(debug=True)

