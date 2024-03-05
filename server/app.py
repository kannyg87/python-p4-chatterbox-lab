from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

def seed_database():
    # Clear existing data
    db.session.query(Message).delete()

    # Create new messages
    message1 = Message(body="Hello world!", username="user1")
    message2 = Message(body="How are you?", username="user2")
    message3 = Message(body="This is a test message", username="user3")

    # Add messages to session
    db.session.add_all([message1, message2, message3])

    # Commit the session
    db.session.commit()

@app.route('/messages',methods=['GET','POST'])
def messages():
    if request.method == "GET":
        messages = [msg.to_dict() for msg in Message.query.all()]
        return make_response( messages, 200 )

# @app.route('/messages', methods=['POST'])
# def create_message():
    elif request.method == "POST":
        new_msg = Message(
            # id = request.form.get("id"),
            body = request.get_json()["body"],
            username=request.get_json()["username"],
            )

        db.session.add(new_msg)
        db.session.commit()

        msg_dict = new_msg.to_dict()

        response = make_response(
                msg_dict,
                201
            )

        return response

@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    msg = Message.query.filter(Message.id == id).first()
    for attr in request.get_json():
            setattr(msg, attr, request.get_json()[attr])

            db.session.add(msg)
            db.session.commit()

            msg_dict = msg.to_dict()

            response = make_response(
                msg_dict,
                200
            )

            return response

@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    msg = Message.query.filter_by(id=id).first()

    if not msg:
        response_body = {
            "message": "Message good not found."
        }
        return make_response(jsonify(response_body), 404)

    db.session.delete(msg)
    db.session.commit()

    response_body = {
        "delete_successful": True,
        "message": f"Message with ID {id} deleted."
    }

    return make_response(jsonify(response_body), 200)

if __name__ == '__main__':
    with app.app_context():
        seed_database()
    app.run(port=5555)
