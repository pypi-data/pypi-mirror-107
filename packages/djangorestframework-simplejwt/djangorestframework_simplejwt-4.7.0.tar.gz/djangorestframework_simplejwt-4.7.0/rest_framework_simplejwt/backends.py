import jwt
from django.utils.translation import gettext_lazy as _
from jwt import InvalidAlgorithmError, InvalidTokenError, algorithms

from .exceptions import TokenBackendError
from .utils import format_lazy

ALLOWED_ALGORITHMS = (
    'HS256',
    'HS384',
    'HS512',
    'RS256',
    'RS384',
    'RS512',
)


class TokenBackend:
    def __init__(self, algorithm, signing_key=None, verifying_key=None, audience=None, issuer=None):
        self._validate_algorithm(algorithm)

        self.algorithm = algorithm
        self.signing_key = signing_key
        self.audience = audience
        self.issuer = issuer
        if algorithm.startswith('HS'):
            self.verifying_key = signing_key
        else:
            self.verifying_key = verifying_key

    def _validate_algorithm(self, algorithm):
        """
        Ensure that the nominated algorithm is recognized, and that cryptography is installed for those
        algorithms that require it
        """
        if algorithm not in ALLOWED_ALGORITHMS:
            raise TokenBackendError(format_lazy(_("Unrecognized algorithm type '{}'"), algorithm))

        if algorithm in algorithms.requires_cryptography and not algorithms.has_crypto:
            raise TokenBackendError(format_lazy(_("You must have cryptography installed to use {}."), algorithm))

    def encode(self, payload):
        """
        Returns an encoded token for the given payload dictionary.
        """
        jwt_payload = payload.copy()
        if self.audience is not None:
            jwt_payload['aud'] = self.audience
        if self.issuer is not None:
            jwt_payload['iss'] = self.issuer

        token = jwt.encode(jwt_payload, self.signing_key, algorithm=self.algorithm)
        if isinstance(token, bytes):
            # For PyJWT <= 1.7.1
            return token.decode('utf-8')
        # For PyJWT >= 2.0.0a1
        return token

    def decode(self, token, verify=True):
        """
        Performs a validation of the given token and returns its payload
        dictionary.

        Raises a `TokenBackendError` if the token is malformed, if its
        signature check fails, or if its 'exp' claim indicates it has expired.
        """
        try:
            return jwt.decode(
                token, self.verifying_key, algorithms=[self.algorithm], verify=verify,
                audience=self.audience, issuer=self.issuer,
                options={'verify_aud': self.audience is not None, "verify_signature": verify}
            )
        except InvalidAlgorithmError as ex:
            raise TokenBackendError(_('Invalid algorithm specified')) from ex
        except InvalidTokenError:
            raise TokenBackendError(_('Token is invalid or expired'))
