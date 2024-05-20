from flask import Flask, request, render_template, redirect

app = Flask(__name__)



@app.route('/', methods=['GET', 'POST'])
def index():
    bot_response = "Bonjour"
    if request.method == 'POST':
        user_message = request.form['message']
        # Traitement du message de l'utilisateur ici
        bot_response = "Je suis un chatbot, je n'ai pas répondu à votre message."
        print(bot_response)
        return render_template("index.html", bot=bot_response)
    return render_template('index.html', bot=bot_response)

if __name__ == "__main__":
    app.run(debug=True)
    