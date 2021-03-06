import re

import pytest

from mimesis import Cryptographic
from mimesis.enums import Algorithm
from mimesis.exceptions import NonEnumerableError

from . import patterns


class TestCryptographic(object):

    @pytest.fixture
    def crypto(self):
        return Cryptographic()

    def test_str(self, crypto):
        assert re.match(patterns.PROVIDER_STR_REGEX, str(crypto))

    def test_uuid(self, crypto):
        assert re.match(patterns.UUID_REGEX, crypto.uuid())

    @pytest.mark.parametrize(
        'algorithm, length', [
            (Algorithm.MD5, 32),
            (Algorithm.SHA1, 40),
            (Algorithm.SHA224, 56),
            (Algorithm.SHA256, 64),
            (Algorithm.SHA384, 96),
            (Algorithm.SHA512, 128),
        ],
    )
    def test_hash(self, crypto, algorithm, length):
        result = crypto.hash(algorithm=algorithm)
        assert len(result) == length

    def test_hash_non_enum(self, crypto):
        with pytest.raises(NonEnumerableError):
            crypto.hash(algorithm='nil')

    def test_bytes(self, crypto):
        result = crypto.bytes(entropy=64)
        assert result is not None
        assert isinstance(result, bytes)

    def test_token(self, crypto):
        result = crypto.token(entropy=16)
        # Each byte converted to two hex digits.
        assert len(result) == 32
        assert isinstance(result, str)

    def test_salt(self, crypto):
        result = crypto.salt()
        assert result is not None
        assert len(result) == 16

    @pytest.mark.parametrize(
        'length', [
            8,
            16,
        ],
    )
    def test_mnemonic_phrase(self, crypto, length):
        result = crypto.mnemonic_phrase(length=length)
        assert isinstance(result, str)
        result = result.split(' ')
        assert len(result) == length


class TestSeededCryptographic(object):

    @pytest.fixture
    def c1(self, seed):
        return Cryptographic(seed=seed)

    @pytest.fixture
    def c2(self, seed):
        return Cryptographic(seed=seed)

    def test_uuid(self, c1, c2):
        assert c1.uuid() == c2.uuid()

    def test_hash(self, c1, c2):
        assert c1.hash() == c2.hash()
        assert c1.hash(algorithm=Algorithm.SHA512) == \
               c2.hash(algorithm=Algorithm.SHA512)

    def test_bytes(self, c1, c2):
        assert c1.bytes() == c2.bytes()
        assert c1.bytes(entropy=16) == c2.bytes(entropy=16)

    def test_token(self, c1, c2):
        assert c1.token() == c2.token()
        assert c1.token(entropy=16) == c2.token(entropy=16)

    def test_salt(self, c1, c2):
        assert c1.salt() == c2.salt()

    def test_mnemonic_phrase(self, c1, c2):
        assert c1.mnemonic_phrase() == c2.mnemonic_phrase()
        assert c1.mnemonic_phrase(length=16) == \
               c2.mnemonic_phrase(length=16)
