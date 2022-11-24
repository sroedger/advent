#!/usr/bin/env python3
import os
import argparse
from pathlib import Path
from typing import Any, Optional, Union
import httpx


class DotEnv:
    """A skinny/limited version of `python-dotenv`"""

    def __init__(self) -> None:
        """Not reusable, specifically looks at this file"""
        self._file = Path(__file__).parent.joinpath(".env")

    def parse(self) -> dict[str, str]:
        parsed = {}
        self._file.touch(exist_ok=True)
        with self._file.open("r") as f:
            lines = f.readlines()
        for line in lines:
            if (len(line) > 0) and (not line.startswith("#")) and ("=" in line):
                # not a comment and contains an equal
                key, value = line.split("=")
                key, value = key.strip().upper(), value.strip()
                parsed[key] = value
                # if key.isidentifier() and value.isidentifier():
                #    parsed[key] = value
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
        if value is None:
            return
        key, value = str(key).strip().upper(), str(value).strip()
        parsed = self.parse()
        parsed[key] = value
        os.environ.update(parsed)
        lines = [f"{k}={v}\n" for k, v in parsed.items()]
        self._file.unlink(missing_ok=True)
        self._file.touch()
        with self._file.open("w") as f:
            f.writelines(lines)

    def __repr__(self) -> str:
        parsed = self.parse()
        lines = [f"{k}={v}" for k, v in parsed.items()]
        return f"<.env: { ','.join(lines) }>"


def get_template(name: str):
    from jinja2 import Environment, FileSystemLoader

    environment = Environment(loader=FileSystemLoader("./template"))
    return environment.get_template(name)


def make_template(context: dict[str, Any]) -> None:
    py_file: Path = context["puzzle_path"].joinpath("main.py")
    if context.get("force", False):
        py_file.unlink(missing_ok=True)
    if not py_file.exists():
        template = get_template("main.py")
        py_file.write_text(template.render(context))


def make_readme(context: dict[str, Any]) -> None:
    def md(text: str) -> str:
        from bs4 import BeautifulSoup
        from markdownify import MarkdownConverter

        result = []
        for soup in BeautifulSoup(text, "html.parser").find_all("article"):
            result.append(MarkdownConverter().convert_soup(soup))
        return "\n".join(result)

    template = get_template("README.md")
    file_path: Path = context["puzzle_path"].joinpath("README.md")
    if context.get("force", False):
        file_path.unlink(missing_ok=True)
    if not file_path.exists():
        response = get_request(context, "url")
        context["readme_md"] = md(response.text)
        file_path.write_text(template.render(context))


def run_tests(context: dict[str, Any]) -> None:
    import subprocess

    files = [file for file in context["puzzle_path"].iterdir() if file.suffix == ".py"]
    subprocess.call(["pytest", "--tb=short", *files])


def get_token() -> Union[str, None]:
    return None


def get_request(context: dict[str, Any], endpoint_name: str) -> httpx.Response:
    token = context.get("token", None)
    url = context.get(endpoint_name, None)
    assert token is not None, "no token"
    assert url is not None, "no url"
    response = httpx.get(url=url, cookies={"session": token})
    response.raise_for_status()
    return response


def get_data(context: dict[str, Any]) -> None:
    data_path: Path = context["puzzle_path"].joinpath("input.txt")
    if data_path.exists() and not context.get("force", False):
        return
    data_path.unlink(missing_ok=True)
    response = get_request(context, "data_url")
    data_path.write_text(response.text)


def run_main(context: dict[str, Any]) -> None:
    import sys
    import subprocess

    path: Path = context["puzzle_path"].joinpath("main.py")
    assert path.exists()

    subprocess.call([sys.executable, path])


def get_context(args: Optional[dict[str, Any]] = None) -> dict[str, Any]:
    dot_env = DotEnv()
    dot_env.load()
    context = {}

    def sync_values(dict_key: str, env_key: str, _type=str) -> Union[str, int]:
        for value in (context.get(dict_key, None), os.environ.get(env_key, None)):
            if value is not None:
                try:
                    value = _type(value)
                    break
                except ValueError:
                    pass
        context[dict_key] = value
        dot_env.set_value(env_key, value)
        return value

    if args is not None:
        context.update(args)
    year = sync_values("year", "AOC_CURRENT_YEAR", _type=int)
    day = sync_values("day", "AOC_CURRENT_DAY", _type=int)
    assert year >= 2015 and day >= 1 and day <= 25, "year/day out of range"
    token = sync_values("token", "AOC_SESSION_TOKEN", _type=str)
    if token is None:
        token = get_token()
    puzzle_path = Path(f"./puzzles/{year}_{day:02d}")
    puzzle_path.mkdir(parents=True, exist_ok=True)
    context["puzzle_path"] = puzzle_path.absolute()
    context["url"] = f"https://adventofcode.com/{year}/day/{day}"
    context["data_url"] = f"https://adventofcode.com/{year}/day/{day}/input"
    return context


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", default=None, nargs="?")
    parser.add_argument("--day", default=None, nargs="?")
    parser.add_argument("--token", default=None, nargs="?")
    parser.add_argument("--setup", action="store_true")
    parser.add_argument("--readme", action="store_true")
    parser.add_argument("--data", action="store_true")
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--run", action="store_true")
    args = parser.parse_args()
    context = get_context(vars(args))
    if args.debug:
        print("context:")
        for k, v in context.items():
            print(f"    {k}: {v}")
    if args.setup:
        make_template(context)
    if args.data:
        get_data(context)
    if args.readme:
        make_readme(context)
    if args.run:
        run_main(context)
    if args.test:
        run_tests(context)


if __name__ == "__main__":
    main()
