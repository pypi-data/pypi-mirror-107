"""Format pages."""

import typing

import termcolor
from bs4 import BeautifulSoup


def format_title(title: str) -> str:
    return termcolor.colored(title, attrs=["bold"]) + "\n\n"


def format_link(link: str) -> str:
    #  "\n\n" +

    return termcolor.colored(
        link,
        color="blue",
        attrs=["underline"],
    )


def format_img(img: typing.Optional[str]) -> str:

    if img:
        return img + "\n"
    else:
        #  termcolor.cprint('No Image', color='grey', file=sys.stderr)

        return ""


def html_formatter_walk(root, prefix="") -> str:
    if not root:
        return ""
    elif root.name in (
        "html",
        "body",
        "span",
        "[document]",
    ):
        return "".join(html_formatter_walk(bit) for bit in root).strip()
    elif root.name == "p":
        return "".join(html_formatter_walk(bit) for bit in root) + f"\n{prefix}"
    elif root.name in ("b", "strong"):
        return termcolor.colored(
            "".join(html_formatter_walk(bit) for bit in root),
            attrs=["bold"],
        )
    elif root.name in ("i", "em"):
        return termcolor.colored(
            "".join(html_formatter_walk(bit, prefix=prefix) for bit in root),
            attrs=["italic"],
        )
    elif root.name == "ul":
        return "\n" + "".join(
            html_formatter_walk(bit, prefix=prefix + "  ") for bit in root
        )
    elif root.name == "br":
        return f"\n{prefix}"
    elif root.name == "li":
        return (
            f"{prefix}- "
            + "".join(html_formatter_walk(bit, prefix=prefix + "  ") for bit in root)
            + "\n"
        )
    elif root.name is None:
        if str(root) == "\n":
            return ""

        return str(root).replace("\n", f"\n{prefix}")
    else:
        return root.string


def format_extract_html(extract_html: str) -> str:
    soup = BeautifulSoup(extract_html, parser="html.parser", features="lxml")

    return html_formatter_walk(soup).strip()
