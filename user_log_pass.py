JWT_SECRET = "Tandem"
JWT_ALGORITHM = "HS256"

USERS = {
    "admin": {"password": "admin1", "ROLE": "ADMIN", "GROUPS": ["ADMIN"]},
    "marker": {"password": "marker2121", "ROLE": "MARKER", "GROUPS": ["MARKER"]},
    "owner": {"password": "owner2", "ROLE": "OWNER", "GROUPS": ["OWNER"]},
    "manager": {"password": "manager3", "ROLE": "MANAGER", "GROUPS": ["MANAGER"]},
}
