import renovation
from renovation.utils.auth import check_user_password, get_bearer_token

from pms_app.utils import InvalidCredentials
from .get_me import get_me


async def get_bearer_token_with_password(email: str, pwd: str):
    if not await check_user_password(email, pwd):
        raise InvalidCredentials()

    token = await get_bearer_token(user=email)
    renovation.set_user(email)

    return renovation._dict(
        access_token=token.access_token,
        expires_in=token.expires_in,
        token_type=token.token_type,
        scopes=token.scopes,
        refresh_token=token.refresh_token,
        id_token=token.id_token,
        pms_contact_info=await get_me()
    )
