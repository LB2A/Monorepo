from keycloak import KeycloakOpenID

keycloak_openid = KeycloakOpenID(
    server_url="http://localhost:8080/",
    client_id="admin-cli",
    realm_name="master",
    verify=False,
)

def validate_token(token: str, realm: str, role: str):
    claims = keycloak_openid.userinfo(token)
    if not claims.get("sub"):
        raise PermissionError("Token without 'sub' claim")

    #TODO: enable signature verification
    decoded = keycloak_openid.decode_token(token, key=None)

    iss = decoded.get("iss", "").rstrip("/")
    if not iss.endswith(f"/realms/{realm}"):
        raise PermissionError(f"Token does not belong to realm '{realm}'")

    roles = decoded.get("realm_access", {}).get("roles", [])
    if role not in roles:
        raise PermissionError(f"Role '{role}' missing in realm '{realm}'")

    return True
