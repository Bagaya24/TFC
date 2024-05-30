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


@app.route("/gestion")
def gestion():
    return render_template("bases_des_pages_de_gestion.html")


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

