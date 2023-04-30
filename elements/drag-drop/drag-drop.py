import chevron
import lxml.html
import prairielearn as pl

def render(element_html: str, data: pl.QuestionData) -> str:
    elem = lxml.html.fragment_fromstring(element_html)
    html_params = {}
    with open("drag-drop.mustache", "r") as f:
        return chevron.render(f, html_params).strip()
