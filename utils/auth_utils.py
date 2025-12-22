from firebase_admin import auth, firestore
from datetime import datetime
from utils.firebase_utils import get_db

db = get_db()



def get_email_by_username(username):
    """
    Converts Employee ID / Username → Email
    """

    users_ref = db.collection("users")
    query = users_ref.where("login_id", "==", username).limit(1).stream()

    for doc in query:
        data = doc.to_dict()
        return data.get("email")

    raise Exception("User ID not found or not approved")

def is_valid_asha_employee(employee_id):
    doc = db.collection("asha_registry").document(employee_id).get()
    if not doc.exists:
        return False
    data = doc.to_dict()
    return data.get("active") is True


def register_user(login_id, email, password, role):
    """
    login_id:
      - ASHA  → Employee ID
      - Public → Username
    """

    # Check duplicate login_id
    existing = db.collection("users").where("login_id", "==", login_id).get()
    if existing:
        raise Exception("This ID already exists")

    # ASHA verification
    if role == "asha":
        if not is_valid_asha_employee(login_id):
            raise Exception("Invalid or inactive ASHA Employee ID")
        status = "approved"
    else:
        status = "approved"

    # Firebase Auth (email is mandatory internally)
    user = auth.create_user(
        email=email,
        password=password
    )

    # Store user record
    db.collection("users").document(user.uid).set({
        "login_id": login_id,
        "email": email,
        "role": role,
        "status": status,
        "created_at": datetime.now().isoformat()
    })

    return user.uid


def login_user(login_id, password):
    users = db.collection("users").where("login_id", "==", login_id).get()
    if not users:
        raise Exception("Invalid credentials")

    user_data = users[0].to_dict()

    if user_data["role"] == "asha" and user_data["status"] != "approved":
        raise Exception("ASHA account not approved")

    # Verify Firebase Auth user exists
    auth.get_user_by_email(user_data["email"])

    return (
        users[0].id,
        user_data["role"],
        user_data["login_id"],
        user_data["email"]
    )
