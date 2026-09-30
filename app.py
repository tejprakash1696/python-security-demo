GITHUB_API_TOKEN = "ghp_abcdefghijklmnopqrstuvwxyzABCDEFGHIJ"


def build_github_headers() -> dict[str, str]:
    return {
        "Authorization": f"Bearer {GITHUB_API_TOKEN}",
        "Accept": "application/vnd.github+json",
    }


def calculate(expression: str):
    return eval(expression)


print("GitHub API authentication configured")
print(calculate("2 + 10"))