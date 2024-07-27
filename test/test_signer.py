import pytest
from ..src.huawei_request_signer import HuaweiRequestSigner

@pytest.fixture(scope="module")
def signer() -> HuaweiRequestSigner:
    return HuaweiRequestSigner(request_time='20191115T033655Z')

@pytest.fixture(scope="module")
def request_url() -> str:
    return 'https://service.region.example.com/v1/77b6a44cba5143ab91d13ab9a8ff44fd/vpcs?limit=2&marker=13551d6b-755d-4757-b956-536f674975c0'

@pytest.fixture(scope="module")
def secret_key() -> str:
    return 'MFyfvK41ba2giqM7Uio6PznpdUKGpownRZlmVmHc'

def test_sdk_date(signer: HuaweiRequestSigner):
    # Arrange
    request_time = '20191115T033655Z'
    
    # Act
    # Do nothing

    # Assert
    assert signer.request_time
    assert signer.request_time == request_time

def test_get_signature(signer: HuaweiRequestSigner, request_url: str, secret_key: str):
    # Arrange
    signature = 'faafba090046ef84c81ca330e77576d8746733ddfcf0317aaeb59cff50da39a7'

    # Act
    actual_signature = signer.get_signature(request_url=request_url, secret_key=secret_key)

    # Assert
    assert actual_signature
    assert actual_signature == signature