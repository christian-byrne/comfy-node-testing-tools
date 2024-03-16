from termcolor import colored
import re


def _log(prefix, *args):
    prefix = colored(f"[{prefix}]", "light_magenta")
    out = " ".join([str(a).strip(" ") for a in args])
    if out[0] != "\n":
        out = f"{prefix} {out}"
    out = out.replace("\n", f"\n{prefix} ")
    print(out)


def smart_print(*args):
    def __extract_header(msg: str) -> list[str]:
        separator_candidates = [
            ":",
            "—",
            r"\)",  # Escaped parenthesis
            r"\]",  # Escaped square bracket
            r"\}",  # Escaped curly bracket
            r"\|",
            "-",
            ";",
            "=",
            ">",
            "\t",
            "\n",
            r"\?",  # Escaped question mark
            r"\*",  # Escaped asterisk
            r"\+",  # Escaped plus sign
            ",",
            "~",
            "/",
            r"\\",  # Escaped backslash
            "&",
            "_",
            " ",
            "",
        ]
        split_by_sep = lambda sep: re.split(sep, msg, 1)
        i = 0
        # Proceed through possible separators until one actually separates the message
        while len(split_by_sep(separator_candidates[i])) <= 1:
            i += 1
        separator = separator_candidates[i]
        msg_parts = split_by_sep(separator)
        return [msg_parts[0] + separator, msg_parts[1].strip()]

    msg_parts = " ".join([str(a).strip(" ") for a in args])
    header, msg = __extract_header(msg_parts)
    print(colored(header, "light_green"), msg)
