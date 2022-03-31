import renovation
from renovation.utils.auth import get_bearer_token_against_refresh_token

from .get_me import get_me


async def get_bearer_token_with_refresh_token(refresh_token: str):

    token = await get_bearer_token_against_refresh_token(refresh_token=refresh_token)
    print(token)
    if token.get("error"):
        raise Exception(token.get("error_description"))

    return renovation._dict(
        access_token=token.access_token,
        expires_in=token.expires_in,
        token_type=token.token_type,
        scopes=token.scopes,
        refresh_token=token.refresh_token,
        id_token=token.id_token,
        pms_contact_info=await get_me()
    )
