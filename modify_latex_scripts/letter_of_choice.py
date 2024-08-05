import re
from typing import Any, LiteralString


def sub_letter_of_choice(text: str, pattern: str) -> tuple[str, list[LiteralString | Any]]:

    choice = []

    matches = re.findall(pattern, text, re.DOTALL)
    if matches:
        for match in matches[0]:
            if re.findall(r"[ㄱ-ㅎ가-힣]", match, re.DOTALL):
                choice.append(match)
            else:
                choice.append('$'+match+'$')

    text_modified = re.sub(pattern, '\n'+'-'*10+' 선지 위치 '+'-'*10+'\n', text)

    return text_modified, choice


def letter_of_choice(text: str) -> tuple[str, list[LiteralString | Any], str]:

    pattern1 = (r"(?m)\\\(\\begin.*"
                r"\\text\s*{\s*\(1\)\s*}\s*(?:\\\()*\s*(.*?)\s*(?:\\\))*\s*&\s*"
                r"\\text\s*{\s*\(2\)\s*}\s*(?:\\\()*\s*(.*?)\s*(?:\\\))*\s*&\s*"
                r"\\text\s*{\s*\(3\)\s*}\s*(?:\\\()*\s*(.*?)\s*(?:\\\))*\s*&\s*"
                r"\\text\s*{\s*\(4\)\s*}\s*(?:\\\()*\s*(.*?)\s*(?:\\\))*\s*&\s*"
                r"\\text\s*{\s*\(5\)\s*}\s*(?:\\\()*\s*(.*?)\s*(?:\\\))*(?:\s*\\end{array}\\\))")
    pattern2 = (r"(?m)^\(1\)\s*(?:\\\()*\s*(.*?)(?:\\\))*\s*\\\\\n+"
                r"^\(2\)\s*(?:\\\()*\s*(.*?)(?:\\\))*\s*\\\\\n+"
                r"^\(3\)\s*(?:\\\()*\s*(.*?)(?:\\\))*\s*\\\\\n+"
                r"^\(4\)\s*(?:\\\()*\s*(.*?)(?:\\\))*\s*\\\\\n+"
                r"^\(5\)\s*(?:\\\()*\s*(.*?)(?:\\\))*\s*(?=\s*\n|\Z)")

    form_of_exercise = '객관식'

    text_modified = sub_letter_of_choice(text, pattern1)
    if not text_modified[1]:
        text_modified = sub_letter_of_choice(text, pattern2)

    if not text_modified[1]:
        form_of_exercise = '주관식'

    return text_modified[0], text_modified[1], form_of_exercise


def modify_letter_of_choice(contents: list[str]) -> list[tuple[str, list[Any], str]]:
    contents_modified = []

    for content in contents:
        content.join('\n')
        content = re.sub(r'\n+', '\n', content)
        contents_modified.append(letter_of_choice(content))

    return contents_modified
