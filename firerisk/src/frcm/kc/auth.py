from decouple import config
from keycloak import KeycloakOpenID
from fastapi import HTTPException, status, Depends, Request

from frcm.kc.models import User

keycloak_openid = KeycloakOpenID(
    server_url="http://127.0.0.1:6969", #config("keycloak_url"),
    realm_name="FireGuard",
    client_id=""
)

# Get Token from HTTP Request object of the restapi endpoint
def get_jwttoken(req: Request):
    token = req.headers["Authorization"]
    token = token.split(" ").pop(1)
    print(token)
    return token

async def get_idp_public_key():
    return (
        "-----BEGIN PUBLIC KEY-----\n"
        f"{keycloak_openid.public_key()}"
        "\n-----END PUBLIC KEY-----"
    )

# Decode Token
async def get_payload(token=Depends(get_jwttoken)) -> dict:
    try:
        return keycloak_openid.decode_token(
            token,
            key=await get_idp_public_key(),
            options={
                "verify_signature": True,
                "verify_iss": True,
                "verify_exp": True
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_user_info(payload: dict = Depends(get_payload)) -> User:
    print(payload)
    client_id = payload.get("azp")
    try:
        return User(
            id=payload.get("sub"),
            username=payload.get("preferred_username"),
            first_name=payload.get("given_name"),
            last_name=payload.get("family_name"),
            realm_roles=payload.get("realm_access", {}).get("roles", []),
            client_roles=payload.get("resource_access", {}).get(client_id, {}).get("roles", [])
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )

def verify_user_role(user: User = Depends(get_user_info)) -> bool:
    roles: list = user.realm_roles
    roles.extend(user.client_roles)
    return verify_role(roles, "USER")

def verify_role(roles: list, role: str) -> bool:
    try:
        roles.index(role)
        return True
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized action",
            headers={"WWW-Authenticate": "Bearer"}
        )
