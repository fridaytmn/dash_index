JWT_SECRET = "Tandem"
JWT_ALGORITHM = "HS256"

USERS = {
    "admin": {"password": "admin1", "ROLE": "ADMIN", "GROUPS": ["ADMIN"]},
    "owner": {"password": "owner2", "ROLE": "OWNER", "GROUPS": ["OWNER"]},
    "manager": {"password": "manager3", "ROLE": "MANAGER", "GROUPS": ["MANAGER"]},
}
