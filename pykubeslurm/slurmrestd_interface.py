"""
Core module for Jobbergate API identity management.

Code adapted from the [Cluster Agent](https://github.com/omnivector-solutions/cluster-agent/blob/main/cluster_agent/identity/slurmrestd.py)
project by Omnivector Solutions, LLC.
"""
import sys
import typing
from datetime import datetime, timedelta

import httpx
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTClaimsError, JWTError
from loguru import logger

from pykubeslurm.settings import SETTINGS


def _load_jwt_key_string() -> str:
    """
    Load the Slurmrestd JWT key string from the file system.

    Returns:
        str: The Slurmrestd JWT key string.
    """
    assert hasattr(logger, "focus")  # make mypy happy
    with logger.focus("PyKubeSlurm - Load Slurmrestd JWT Key"):
        try:
            secret_key = open(SETTINGS.SLURMRESTD_JWT_KEY_PATH, "r").read()
        except FileNotFoundError:
            logger.error(
                f"Couldn't find the slurmrestd JWT key file at {SETTINGS.SLURMRESTD_JWT_KEY_PATH}"
            )
            sys.exit(1)
        except PermissionError:
            logger.error(
                f"Couldn't read the slurmrestd JWT key file at {SETTINGS.SLURMRESTD_JWT_KEY_PATH} (missing permissions)"
            )
            sys.exit(1)

    return secret_key


def _load_token_from_cache() -> typing.Union[str, None]:
    """
    Load the slurmrestd auth token from the cache directory.

    Returns:
        str: The Slurmrestd auth token
        None: None if the token is one of the following:
            * Doesn't exist
            * Can't be read
            * Is expired
    """
    token_path = SETTINGS.CACHE_DIR / "slurmrestd/token"
    if not token_path.exists():
        return None

    assert hasattr(logger, "focus")  # make mypy happy
    with logger.focus("PyKubeSlurm - Load Slurmrestd Token from Cache"):
        try:
            token = token_path.read_text().strip()
        except Exception:
            logger.warning(
                f"Couldn't load token from cache file {token_path}. Will acquire a new one"
            )
            return None

    secret_key = _load_jwt_key_string()

    with logger.focus("PyKubeSlurm - Decode Existing Token from Cache"):
        try:
            jwt.decode(
                token,
                secret_key,
                options=dict(verify_signature=False, verify_exp=True, leeway=-10),
            )
        except ExpiredSignatureError:
            logger.warning("Cached token is expired. Will acquire a new one.")
            return None
        except JWTClaimsError:
            logger.warning("Cached token is malformed. Will acquire a new one")
            return None
        except JWTError:
            logger.warning("Cached token is malformed. Will acquire a new one")
            return None

    return token


def _write_token_to_cache(token: str) -> None:
    """
    Write the Slurmrestd token to the cache.

    Args:
        token (str): The Slurmrestd auth token
    """
    assert hasattr(logger, "focus")  # make mypy happy
    with logger.focus("PyKubeSlurm - Write Token to Cache"):
        if not SETTINGS.CACHE_DIR.exists():
            logger.debug("Attempting to create missing cache directory")
            try:
                SETTINGS.CACHE_DIR.mkdir(mode=0o700, parents=True, exist_ok=True)
            except Exception:
                logger.warning(
                    f"Couldn't create missing cache directory {SETTINGS.CACHE_DIR}. Token will not be saved."
                )
                return

        token_path = SETTINGS.CACHE_DIR / "slurmrestd" / "token"
        if not token_path.parent.exists():
            token_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            token_path.write_text(token)
            token_path.chmod(0o600)
        except Exception:
            logger.error(f"Couldn't save token to {token_path}")


def acquire_token(username: str) -> str:
    """
    Generate a JWT token to be used against Slurmrestd.

    Args:
        username: The username which requests will be made on behalf of.
    Returns:
        str: The JWT token.
    """
    assert hasattr(logger, "focus")  # make mypy happy
    with logger.focus("PyKubeSlurm - Generate JWT Token"):
        logger.debug("Attempting to use cached token")
        token = _load_token_from_cache()

        if token is None:
            secret_key = _load_jwt_key_string()

            now = datetime.now()
            payload = {
                "exp": now + timedelta(seconds=SETTINGS.SLURMRESTD_EXP_TIME_IN_SECONDS),
                "iat": now,
                "sun": username,
            }
            token = jwt.encode(payload, secret_key, algorithm="HS256")
            _write_token_to_cache(token)

        logger.debug("Successfully generated auth token")
    return token


def inject_token(
    request: httpx.Request,
    username: typing.Optional[str] = None,
) -> httpx.Request:
    """
    Inject a token based on the provided username into the request.

    For requests that need to use something except the default username,
    this injector should be used at the request level (instead of at client
    initialization), for example:

    ```python
    client.get(url, auth=lambda r: inject_token(r, username=username))
    ```

    Returns:
        httpx.Request: The intercepted request object.
    """
    if username is None:
        username = SETTINGS.SLURMRESTD_USER_TOKEN

    token = _load_token_from_cache()
    if token is None:
        token = acquire_token(username)

    request.headers["x-slurm-user-name"] = username
    request.headers["x-slurm-user-token"] = token
    return request


class BackendClient(httpx.Client):
    """Client extension class to customize log messages and the auth method when a request is made to the Slurmrestd API."""

    _token: typing.Optional[str]

    def __init__(self) -> None:
        self._token = None
        super().__init__(
            base_url=SETTINGS.SLURMRESTD_ENDPOINT,
            auth=inject_token,
            event_hooks=dict(
                request=[self._log_request],
                response=[self._log_response],
            ),
            timeout=SETTINGS.SLURMRESTD_TIMEOUT,
        )

    @staticmethod
    def _log_request(request: httpx.Request) -> None:
        assert hasattr(logger, "focus")  # make mypy happy
        with logger.focus("PyKubeSlurm - Make Request to the Slurmrestd API"):
            logger.debug(f"Making request: {request.method} {request.url}")

    @staticmethod
    def _log_response(response: httpx.Response) -> None:
        assert hasattr(logger, "focus")  # make mypy happy
        with logger.focus("PyKubeSlurm - Request Completed"):
            logger.debug(
                f"Received response: {response.request.method} "
                f"{response.request.url} "
                f"{response.status_code}"
            )


backend_client = BackendClient()
