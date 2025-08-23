

class ChromeProfileNotFoundException(Exception):
    def __init__(self, profile: str) -> None:
        self._profile = profile
        message = f"Chrome profile not found - '{profile}'"
        super().__init__(message)

    @property
    def profile(self) -> str:
        return self._profile

    @profile.setter
    def profile(self, new_profile: str) -> None:
        self._profile = new_profile
