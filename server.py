from flask import Flask, render_template, request, jsonify, Response
import chatbot

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/sendMessage", methods=["POST"])
def mssg():
    print('workin')
    ints = chatbot.predict_class(request.json['message'], chatbot.model)
    statusCode = 200
    if(ints[0]['intent'] == "scheduling_help"):
        statusCode = 201
    chatbotResponse = chatbot.chatbot_response(request.json, ints)
    return Response(chatbotResponse, status=statusCode)
    


if __name__ == "__main__":
    app.run(debug=True)