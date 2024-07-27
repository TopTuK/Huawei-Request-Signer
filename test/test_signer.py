import pytest
from huawei_request_signer import HuaweiRequestSigner

@pytest.fixture(scope="module")
def signer() -> HuaweiRequestSigner:
    return HuaweiRequestSigner

def test_sdk_date(signer: HuaweiRequestSigner):
    pass