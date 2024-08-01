import re


def split_mathpix_tex_source(tex_source):
    contents_split = []
    # 문제 또는 해설의 시작을 표시하는 pattern 정의
    pattern = r'\\\\\n\d{1,2}\s*[\.:]|\n\n\d{1,2}\s*[\.:]|\\item'
    # tex_source에서 문제 또는 해설의 시작을 표시하는 pattern 위치 파악
    matches_point = []
    matches = re.finditer(pattern, tex_source, re.DOTALL)
    for match in matches:
        matches_point.append([match.start(), match.end()])
    # 파악한 위치로 분리 저장
    for i in range(len(matches_point) - 1):
        contents_split.append(tex_source[matches_point[i][1]:matches_point[i + 1][0]])
    contents_split.append(tex_source[matches_point[-1][1]:])

    for i in range(len(matches_point)):
        # \section*{section_title}부터 끝까지 삭제
        contents_split[i] = remove_section_to_end(contents_split[i])
        # 지정된 단어를 포함하는 라인 삭제
        contents_split[i] = remove_lines_with_words(contents_split[i])
    # 18byte 이하인 항목 삭제
    filtered_contents_split = remove_short_items(contents_split)
    # 한글 문자 and 문자($)가 없는 항목 삭제
    contents_split = remove_non_korean_items(filtered_contents_split)
    return contents_split


# \section*{section_title}부터 끝까지 삭제
def remove_section_to_end(text):
    titles_to_remove = ['수학 영역', '공통과목', '미적분']
    # \section*{section_title}부터 끝까지 선택
    section_title = '|'.join(map(re.escape, titles_to_remove))
    pattern = rf'\\section\*{{({section_title})}}.*'
    modified_text = re.sub(pattern, '', text, flags=re.DOTALL)
    return modified_text.strip()


# 지정된 단어를 포함하는 라인 삭제
def remove_lines_with_words(text):
    # 단어 지정
    words_to_remove = \
        ['begin{enumerate}', 'end{enumerate}', 'setcounter{enumi}', 'begin{itemize}',
         'end{itemize}', 'end{document}', '단답형', '선다형', '확인 사항', '답안지의 해당란에',
         '선택한 과목인지 확인하시오', '제2교시 수학 영역', '문제지']
    # 문자열을 줄 단위로 분리
    lines = text.split('\n')
    # 지정된 단어들 중 어느 하나도 포함하지 않는 라인만 선택
    filtered_lines = [line for line in lines if not any(word in line for word in words_to_remove)]
    # 필터링된 라인들을 다시 하나의 문자열로 결합
    return '\n'.join(filtered_lines)


# 18byte 이하인 항목 삭제


def remove_short_items(text_list, min_length=18):
    # 지정된 길이보다 긴 항목만 선택
    return [item for item in text_list if len(item) > min_length]


# 한글 문자 and 문자($)가 없는 항목 삭제


def remove_non_korean_items(text_list):
    # 한글 문자를 포함하는 항목만 선택
    korean_pattern = re.compile('[$가-힣]')
    return [item for item in text_list if korean_pattern.search(item)]
