def slugify(name: str) -> str:
    """Convert a string to a slug format."""
    return name.lower().replace(" ", "-")


def test_slugify():
    assert slugify("Hello World") == "hello-world"
    assert slugify("  Hello   World  ") == "--hello---world--"
