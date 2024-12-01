from pydantic import BaseModel, ValidationError
from hypothesis import given, strategies as st

from specs.validators import http_verbs as hv

import pytest

class HTTPVerbModel(BaseModel):
    verb: hv.HTTPVerb

@pytest.mark.parametrize("verb", hv.HTTP_VERBS)
def test_valid_http_verbs(verb):
    model = HTTPVerbModel(verb=verb)
    assert model.verb == verb

@given(st.text())
def test_random_strings(verb):
    if verb in hv.HTTP_VERBS:
        model = HTTPVerbModel(verb=verb)
        assert model.verb == verb
    else:
        with pytest.raises(ValidationError):
            HTTPVerbModel(verb=verb)

