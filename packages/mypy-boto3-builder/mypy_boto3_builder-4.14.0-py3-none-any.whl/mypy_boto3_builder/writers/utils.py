"""
Jinja2 renderer and black formatter.
"""
import re
import tempfile
from pathlib import Path
from typing import Iterable, Optional

import black
import md_toc
import mdformat
from black import InvalidInput, NothingChanged
from isort.api import Config, sort_code_string

from mypy_boto3_builder.constants import LINE_LENGTH, TEMPLATES_PATH
from mypy_boto3_builder.jinja_manager import JinjaManager
from mypy_boto3_builder.service_name import ServiceName
from mypy_boto3_builder.structures.package import Package


def blackify(content: str, file_path: Path) -> str:
    """
    Format `content` with `black` if `file_path` is `*.py` or `*.pyi`.

    On error writes invalid `content` to `file_path` to check for errors.

    Arguments:
        content -- Python code to format.
        file_path -- Target file path.

    Returns:
        Formatted python code.

    Raises:
        ValueError -- If `content` is not a valid Python code.
    """
    if file_path.suffix not in (".py", ".pyi"):
        return content

    file_mode = black.FileMode(is_pyi=file_path.suffix == ".pyi", line_length=LINE_LENGTH)
    try:
        content = black.format_file_contents(content, fast=True, mode=file_mode)
    except NothingChanged:
        pass
    except (IndentationError, InvalidInput) as e:
        file_path.write_text(content)
        raise ValueError(f"Cannot parse {file_path}: {e}") from e

    return content


def sort_imports(
    content: str, module_name: str, extension: str = "py", third_party: Iterable[str] = ()
) -> str:
    known_third_party = list(third_party) or [
        "boto3",
        "botocore",
        "typing_extensions",
        "mypy_boto3",
    ]
    if module_name in known_third_party:
        known_third_party.remove(module_name)

    result = sort_code_string(
        code=content,
        extension=extension,
        config=Config(
            profile="black",
            known_first_party=[module_name],
            known_third_party=known_third_party,
            line_length=LINE_LENGTH,
        ),
    )
    return result or ""


def render_jinja2_template(
    template_path: Path,
    package: Optional[Package] = None,
    service_name: Optional[ServiceName] = None,
) -> str:
    """
    Render Jinja2 template to a string.

    Arguments:
        template_path -- Relative path to template in `TEMPLATES_PATH`
        module -- Module record.
        service_name -- ServiceName instance.

    Returns:
        A rendered template.
    """
    template_full_path = TEMPLATES_PATH / template_path
    if not template_full_path.exists():
        raise ValueError(f"Template {template_path} not found")

    template = JinjaManager.get_environment().get_template(template_path.as_posix())
    return template.render(package=package, service_name=service_name)


def insert_md_toc(text: str) -> str:
    """
    Insert Table of Contents before the first second-level header.
    """
    headers = {}
    header_re = re.compile(r"\s*\- \[(.+)\]\(#(.+)\)")
    with tempfile.NamedTemporaryFile("w+") as f:
        f.write(text)
        f.flush()
        toc_lines = md_toc.build_toc(f.name).splitlines()
        for toc_line in toc_lines:
            match = header_re.match(toc_line)
            if match:
                headers[match.groups()[0]] = match.groups()[1]

    lines = text.splitlines()
    result = []
    inserted = False
    for line in lines:
        if not inserted and line.startswith("## "):
            result.extend(toc_lines)
            result.append("")
            inserted = True

        result.append(line)

    if not inserted:
        result.extend(toc_lines)
        result.append("")

    return "\n".join(result)


def format_md(text: str) -> str:
    """
    Format MarkDown with mdformat.
    """
    return mdformat.text(
        text,
        options={
            "wrap": 79,
        },
    )


def fix_pypi_headers(text: str) -> str:
    """
    Fix headers for PyPi links to work.
    """
    headers = {}
    header_re = re.compile(r"\s*\- \[(.+)\]\(#(.+)\)")
    with tempfile.NamedTemporaryFile("w+") as f:
        f.write(text)
        f.flush()
        toc_lines = md_toc.build_toc(f.name).splitlines()
        for toc_line in toc_lines:
            match = header_re.match(toc_line)
            if match:
                headers[match.groups()[0]] = match.groups()[1]

    lines = text.splitlines()
    result = []
    for line in lines:
        header = line.lstrip("#").strip()
        if header and header in headers:
            anchor = headers[header]
            result.append(f'{line}<a id="{anchor}"></a>')
            continue

        result.append(line)

    return "\n".join(result)
