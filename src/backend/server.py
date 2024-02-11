from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

file_path = "src/backend/data.json"


def readJSON():
    with open(file_path, "r") as file:
        try:
            file_data = json.load(file)
            return file_data
        except (FileNotFoundError, json.JSONDecodeError):
            print("errore")
            rewriteJSON([])
            return []


def updateJSON(file_data, data):
    file_data.append(data)
    print(file_data)  # Check if data is not empty
    return file_data


def rewriteJSON(dataToSave):
    with open(file_path, "w") as file:
        json.dump(dataToSave, file, indent=2)


def searchForMatches(data, file_data):
    for i in file_data:
        #print(i["username"], i["email"])
        if data["username"] == i["username"] or data["email"] == i["email"]:
            return True

    return False


@app.route("/", methods=["GET", "POST"])
def hello():
    if request.method == "GET":
        return jsonify(message="Hello, World!")
    elif request.method == "POST":
        # data is sent in the request; file_data is none by default, it will be updated
        data = request.json
        print("data:", data)

        # Нужно заново считать json, записать в массив новые данные и снова сохранить в json
        try:
            file_data = readJSON()
            user_exists = searchForMatches(data, file_data)
            if not user_exists:
                file_data = updateJSON(file_data, data)
                rewriteJSON(file_data)
            else:
                return jsonify(message=f"you're late. Username or email already taken")
            
        except Exception as e:
            print(f"Error writing to file: {e}")

        return jsonify(message=f"User registered successfully")


if __name__ == "__main__":
    app.run(debug=True)
