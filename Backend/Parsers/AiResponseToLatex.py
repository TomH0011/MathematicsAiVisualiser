from Backend.Parsers import LatexToEnglish
from Backend.Parsers.LatexToEnglish import tokenise_latex


def parse_latex_response(response: str) -> str:
    if "**LaTeX Output**" in response:
        start = response.find("\documentclass{article}")
        end = response.find("\end{document}")

        to_be_parsed = response[start:end]
        print(to_be_parsed)

        tokens = tokenise_latex(to_be_parsed)
        ast = parse(tokens)


    else:
        return "Response Inocrrectly Formatted - **Latex Output** Not found"
