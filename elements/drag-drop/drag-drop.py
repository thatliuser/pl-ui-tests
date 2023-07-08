import chevron
from lxml.html import fragment_fromstring, HtmlElement
import prairielearn as pl
from typing import Dict, Optional

# Option to answer map
OptionMap = Dict[str, Optional[str]]

def get_matches(element: HtmlElement) -> OptionMap:
    map: OptionMap = {}

    # Sort the elements so that pl-options come first.
    children = element[:]
    children.sort(key=lambda child: child.tag)

    for child in children:
        if child.tag in ["pl-option", "pl_option"]:
            name = pl.inner_html(child)
            # This option has no corresponding answer
            map[name] = None
        elif child.tag in ["pl-statement", "pl_statement"]:
            # Ensure that there is a matching option specified
            pl.check_attribs(child, ["match"], [])
            name = pl.get_string_attrib(child, "match")
            answer = pl.inner_html(child)
            # The match option specified is the answer to this field
            map[name] = answer

    return map

def prepare(element_html: str, data: pl.QuestionData) -> None:
    element = fragment_fromstring(element_html)

    # TODO: Improve attribs (https://github.com/PrairieLearn/PrairieLearn/blob/master/elements/pl-matching/pl-matching.py)
    # Throws error if element is invalid
    """ def check_attribs(
        element: lxml.html.HtmlElement,
        required_attribs: list[str],
        optional_attribs: list[str],
    ) -> None """
    pl.check_attribs(element, ["answers-name"], [])

    # Get the name we should put under data["params"]
    # If answers-name="answers", then name = "answers"
    """ def get_string_attrib(
        element: lxml.html.HtmlElement,
        name: str
    ) -> str """
    name = pl.get_string_attrib(element, "answers-name")

    # Get option to answer map
    matches = get_matches(element)

    for option, answer in matches.items():
        if answer is not None:
            data["correct_answers"][answer] = option

    data["params"][name] = matches

def render(element_html: str, data: pl.QuestionData) -> str:
    element = fragment_fromstring(element_html)
    name = pl.get_string_attrib(element, "answers-name")

    matches: OptionMap = data["params"][name]
    answers = []
    options = []

    for option, answer in matches.items():
        options.append({
            "name": option
        })
        if answer is not None:
            answers.append({
                "name": answer
            })

    html_params = {
        "answers": answers,
        "options": options,
    }

    with open("drag-drop.mustache", "r") as f:
        return chevron.render(f, html_params).strip()
