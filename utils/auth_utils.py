import firebase_admin
from firebase_admin import auth, firestore

db = firestore.client()

def register_user(email, password, role):
    user = auth.create_user(email=email, password=password)
    db.collection("users").document(user.uid).set({
        "email": email,
        "role": role
    })

def authenticate_user(email, password):
    users = db.collection("users").where("email", "==", email).get()
    if users:
        return users[0].to_dict()
    return None
