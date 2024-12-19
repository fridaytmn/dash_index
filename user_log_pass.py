JWT_SECRET = "Tandem"
JWT_ALGORITHM = "HS256"

USERS = {
    "admin": {"password": "admin123", "ROLE": "ADMIN", "GROUPS": ["ADMIN"]},
    "owner": {"password": "owner123", "ROLE": "OWNER", "GROUPS": ["OWNER"]},
    "manager": {"password": "manager123", "ROLE": "MANAGER", "GROUPS": ["MANAGER"]},
}
