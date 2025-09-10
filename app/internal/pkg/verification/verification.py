""" """

import secrets


async def create_verification_code() -> str:
    code = "".join(str(secrets.randbelow(10)) for _ in range(6))
    return code
