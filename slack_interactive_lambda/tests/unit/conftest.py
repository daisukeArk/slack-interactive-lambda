from dataclasses import dataclass

import pytest


@pytest.fixture
def lambda_context():
    @dataclass
    class LambdaContext:
        function_name: str = "dummy"
        aws_request_id: str = "88888888-4444-4444-4444-121212121212"
        invoked_function_arn: str = "arn:aws:lambda:us-east-1:123456789012:function:dummy"
        memory_limit_in_mb: int = 128

    return LambdaContext()
