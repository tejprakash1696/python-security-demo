import os


GITHUB_API_TOKEN = os.environ.get("GITHUB_API_TOKEN")

def build_github_headers() -> dict[str, str]:
    if not GITHUB_API_TOKEN:
        raise RuntimeError("GitHub API token is missing")

    return {
        "Authorization": f"Bearer {GITHUB_API_TOKEN}",
        "Accept": "application/vnd.github+json",
    }


def calculate_total(quantity: int, price: float) -> float:
    return quantity * price


print("GitHub API authentication configured")
print(calculate_total("2 + 10"))