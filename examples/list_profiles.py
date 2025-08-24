"""List the available Chrome profiles for the current user."""

from chpass.services.chrome import list_profiles


def main() -> None:
    """Print available Chrome profiles for the current user."""
    list_profiles()


if __name__ == "__main__":
    main()
