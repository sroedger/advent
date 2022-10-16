import os
import argparse
from pathlib import Path


class DotEnv:
    """A skinny/limited version of `python-dotenv`"""

    def __init__(self) -> None:
        """Not reusable, specifically looks at this file"""
        self._file = Path(__file__).parent.joinpath(".env")

    def parse(self) -> dict[str, str]:
        parsed = {}
        self._file.touch()
        with self._file.open("r") as f:
            lines = f.readlines()
        for line in lines:
            if (len(line) > 0) and (not line.startswith("#")) and ("=" in line):
                # not a comment and contains and equal
                key, value = line.split("=")
                key, value = key.strip().upper(), value.strip()
                if key.isidentifier() and value.isidentifier():
                    parsed[key] = value
        return parsed

    def load(self) -> None:
        """Open file, parse, then load to `os.environ`"""
        parsed = self.parse()
        os.environ.update(parsed)

    def set_value(self, key: str, value: str) -> None:
        """
        Write a key/value pair to the .env file.
        Does not preserve comments.
        """
        key, value = key.strip().upper(), value.strip()
        if not (key.isidentifier() and value.isidentifier()):
            return
        parsed = self.parse()
        parsed[key] = value
        os.environ.update(parsed)
        lines = [f"{k}={v}\n" for k, v in parsed.items()]
        self._file.unlink()
        self._file.touch()
        with self._file.open("w") as f:
            f.writelines(lines)

    def __repr__(self) -> str:
        parsed = self.parse()
        lines = [f"{k}={v}" for k, v in parsed.items()]
        return f"<.env: { ','.join(lines) }>"


DOT_ENV = DotEnv()


def main() -> None:
    parser = argparse.ArgumentParser()
    args = parser.parse_args()


if __name__ == "__main__":
    DOT_ENV.load()
    main()
