class MockedRequest():
    """
    For use with testing.
    """
    def __init__(self, user: str, data: dict):
        self.user = user
        self.data = data