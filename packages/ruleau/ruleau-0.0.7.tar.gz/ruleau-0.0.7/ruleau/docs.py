import argparse
import importlib
import re
import sys
from argparse import Namespace
from os import mkdir, path
from typing import AnyStr

from jinja2 import Template


def trim(docstring):
    """trim function implementation from PEP-257
    https://www.python.org/dev/peps/pep-0257/#id18

    :param docstring: Docstring for a function
    """
    if not docstring:
        return ""
    # Convert tabs to spaces (following the normal Python rules)
    # and split into a list of lines:
    lines = docstring.expandtabs().splitlines()
    # Determine minimum indentation (first line doesn't count):
    indent = sys.maxsize
    for line in lines[1:]:
        stripped = line.lstrip()
        if stripped:
            indent = min(indent, len(line) - len(stripped))
    # Remove indentation (first line is special):
    trimmed = [lines[0].strip()]
    if indent < sys.maxsize:  # pragma: no cover
        for line in lines[1:]:
            trimmed.append(line[indent:].rstrip())
    # Strip off trailing and leading blank lines:
    while trimmed and not trimmed[-1]:
        trimmed.pop()
    while trimmed and not trimmed[0]:
        trimmed.pop(0)

    if "\n" in docstring:
        trimmed.append("")
    # Return a single string:
    return "\n".join(trimmed)


def description(docstring: AnyStr) -> AnyStr:
    """Takes a rule docstring, and returns just the lines
    representing a description

    :param docstring: Docstring for a function
    """
    result = trim(docstring or "")
    if "\n\n" in result:
        return result[: result.index("\n\n")]
    return result


def parameters(docstring: AnyStr):
    """Parse list of parameters out of the docstring

    :param docstring: The docstring of the rule
    :returns: [{"name": ..., "description": ...}, ...]
    """
    PARAM_REGEX = re.compile(
        ":(?P<name>[\*\s\w]+): (?P<description>.*?)\Z"  # noqa: W605
    )

    params = {}
    if docstring:
        lines = docstring.split("\n")
        for line in lines:
            match = PARAM_REGEX.findall(line.strip())
            if match:
                param_name, param_description = match[0]
                params.update({param_name: param_description})

    return params


def title(name: AnyStr) -> AnyStr:
    """Convert the function name into a title

    :param name: Name of a function
    """
    return name.replace("_", " ").title()


def generate_documentation(rules) -> AnyStr:
    """Returns a HTML string, documenting the passed in rule and its dependants

    :param rules: List of rules to generate document of
    """

    with open(
        path.join(path.dirname(path.realpath(__file__)), "html", "documentation.html")
    ) as f:
        doc_template = Template(f.read())

    enriched_rules = [rule.parse() for rule in rules]
    return doc_template.render(rules=enriched_rules)


def render_doc_for_module(module_file) -> AnyStr:
    """Render the documentation from a rule module
    :param module_file:
    :return:
    """
    spec = importlib.util.spec_from_file_location(module_file, module_file)
    config = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config)

    # Pick rules to document
    rules = [
        rule
        for rule in vars(config).values()
        if getattr(type(rule), "__name__", None) == "Rule"
    ]
    if not rules:
        raise Exception("No rules found in {}.".format(module_file))

    return generate_documentation(rules)


def generate_and_save_to_file(input_files, output_dir) -> int:
    """Generate the documentation and save to a file in provided output dir
    :param input_files: Rule modules provided by user via CLI
    :param output_dir: Output directory of generated HTML file
    :return:
    """
    generated_docs = []

    if len(input_files) == 0:
        raise Exception("No file(s) supplied to generate documentation for.")

    if not path.exists(output_dir):
        mkdir(output_dir)

    for target_file in input_files:
        if not path.exists(target_file):
            raise ValueError(f"{target_file} does not exist")

        documentation = render_doc_for_module(target_file)

        output_filename = path.join(
            output_dir, "{}.html".format(path.basename(target_file).split(".")[0])
        )

        with open(output_filename, "w") as f:
            f.write(documentation)
        generated_docs.append(output_filename)

    print(
        f"{len(generated_docs)} doc{'s' if len(generated_docs) > 1 else ''} generated."
    )
    print("\n".join(generated_docs))

    return 0


def get_arguments(args) -> Namespace:
    """Parses arguments for the ruleau-docs command
    :param args:
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-dir",
        dest="output_dir",
        default="./",
        help="Directory for generated documents",
    )
    parser.add_argument("files", nargs="*")
    return parser.parse_args(args)


def main() -> int:  # pragma: no cover
    """Console script for deft document generation.
    USAGE:
    ```bash
    $ ruleau-docs [--output-dir=<argument>] filename ...
    ```
    """
    args = get_arguments(sys.argv[1:])
    return generate_and_save_to_file(args.files, args.output_dir)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
