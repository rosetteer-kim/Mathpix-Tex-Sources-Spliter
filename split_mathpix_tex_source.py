# Source file 구조: (쓰레기) (marker) (content) (marker) (content) ... (marker) (content) (\end{document})
# (marker)의 종류 2024년 08월 03일 버전
#   1. r'\\\\\n\d{1,2}\s*[\.:\)]|\n\n\d{1,2}\s*[\.:\)]|\\section\*\{\d{1,2}\.|\\section\*\{\d{1,2}\)'
#   2. enumerate 환경 내부의 \item
#   3. (시대인재 해설)
#      r'\\section\*\{\d{1,2}\}|\n\n\d{1,2}\n|\\\\\n\d{1,2}\n'
# (marker)들의 시작 위치와 끝 위치를 찾아서 (content)들을 추출
#
#
#

import re
from collections.abc import Callable
from typing import Optional

MarkerLocationAdjustment = Callable[[int], int]
EnumMarkerLocations = Callable[[Optional[MarkerLocationAdjustment],
                                Optional[MarkerLocationAdjustment]], list[tuple[int, int]]]


def enum_marker_locations(text: str, marker_pattern: str) -> EnumMarkerLocations:
    def gen_marker_locations(make_start: MarkerLocationAdjustment,
                             make_end: MarkerLocationAdjustment) -> list[tuple[int, int]]:

        matches_point = []
        matches = re.finditer(marker_pattern, text, re.DOTALL)

        for match in matches:
            start = make_start(match.start())
            end = make_end(match.end())
            match_tuple = (start, end)
            matches_point.append(match_tuple)

        return matches_point

    return gen_marker_locations


def find_marker_type1(tex_src: str):
    marker_pattern_type1 = \
        r'\\\\\n\d{1,2}\s*[\.:\)]|\n\n\d{1,2}\s*[\.:\)]|\\section\*\{\d{1,2}\.|\\section\*\{\d{1,2}\)'
    gen_marker_position = enum_marker_locations(tex_src, marker_pattern_type1)
    marker_positions = gen_marker_position(lambda x: x, lambda x: x)
    return marker_positions


def find_marker_type2(tex_src: str):
    pattern_high_level = r'\\begin{enumerate}.*?\\end{enumerate}'
    marker_pattern_type2 = r'\\item'
    marker_positions = []
    for enum_match in re.finditer(pattern_high_level, tex_src, re.DOTALL):
        enum_start = enum_match.start()
        enum_text = enum_match.group()
        gen_marker_position = enum_marker_locations(enum_text, marker_pattern_type2)
        marker_position = gen_marker_position(lambda x: enum_start + x, lambda x: enum_start + x)
        marker_positions += marker_position
    return marker_positions


# 시대인재 해설
def find_marker_type3(tex_src: str):
    marker_pattern_type3 = \
        r'\\section\*\{\d{1,2}\}|\n\n\d{1,2}\n|\\\\\n\d{1,2}\n'
    gen_marker_position = enum_marker_locations(tex_src, marker_pattern_type3)
    marker_positions = gen_marker_position(lambda x: x, lambda x: x)
    return marker_positions


def split_mathpix_tex_source(tex_src: str):
    pattern = r'\\begin\{verbatim\}|\\end\{verbatim\}|\\section\*\{수학 영역\}'
    tex_src_screened = re.sub(pattern, '', tex_src)
    tex_src_screened = re.sub('ᄀ', 'ㄱ', tex_src_screened)
    tex_src_screened = re.sub('ᄂ', 'ㄴ', tex_src_screened)
    tex_src_screened = re.sub('ᄃ', 'ㄷ', tex_src_screened)
    return split_tex_source(tex_src_screened)


def split_tex_source(tex_src: str):
    marker_positions = find_marker_type1(tex_src) + find_marker_type2(tex_src) + find_marker_type3(tex_src)
    marker_positions.sort()

    # 파악한 위치로 분리 저장
    contents_split = []
    for i in range(len(marker_positions) - 1):
        contents_split.append(tex_src[marker_positions[i][1]:marker_positions[i + 1][0]])
    contents_split.append(tex_src[marker_positions[-1][1]:])

    for i in range(len(marker_positions)):
        # 첫 줄에서 닫힌 중괄호가 하나 더 많은 항목 수정
        contents_split[i] = remove_extra_closing_brace(contents_split[i])
        # \section*{section_title}부터 끝까지 삭제
        contents_split[i] = remove_section_to_end(contents_split[i])
        # 지정된 단어를 포함하는 라인 삭제
        contents_split[i] = remove_lines_with_words(contents_split[i])
    # 18byte 이하인 항목 삭제
    filtered_contents_split = remove_short_items(contents_split)
    # 한글 문자 and 문자($)가 없는 항목 삭제
    contents_split = remove_non_korean_items(filtered_contents_split)
    return contents_split


# 첫 줄에서 닫힌 중괄호가 하나 더 많은 항목 수정
def remove_extra_closing_brace(text: str):
    lines = text.split('\n', 1)
    first_line = lines[0]

    open_count = first_line.count('{')
    close_count = first_line.count('}')

    if close_count == open_count + 1:
        # 마지막 중괄호 제거
        first_line = first_line.rsplit('}', 1)[0]
    # 수정된 첫 줄과 나머지 연결 후 리턴
    return first_line + ('\n' + lines[1] if len(lines) > 1 else '')


# \section*{section_title}부터 끝까지 삭제
def remove_section_to_end(text: str):
    # titles_to_remove = ['수학 영역', '공통과목', '미적분', '* 확인 사항']
    titles_to_remove = ['공통과목', '미적분', '* 확인 사항', '확률과 통계']
    # \section*{section_title}부터 끝까지 선택
    section_title = '|'.join(map(re.escape, titles_to_remove))
    pattern = rf'\\section\*{{({section_title})}}.*'
    modified_text = re.sub(pattern, '', text, flags=re.DOTALL)
    return modified_text.strip()


# 지정된 단어를 포함하는 라인 삭제
def remove_lines_with_words(text: str):
    # 단어 지정
    words_to_remove = \
        ['begin{enumerate}', 'end{enumerate}', 'setcounter{enumi}', 'begin{itemize}',
         'end{itemize}', 'end{document}', '단답형', '선다형', '확인 사항', '답안지의 해당란에',
         '선택한 과목인지 확인하시오', '제2교시 수학 영역', '문제지', '수 학 영 역 ']
    # 문자열을 줄 단위로 분리
    lines = text.split('\n')
    # 지정된 단어들 중 어느 하나도 포함하지 않는 라인만 선택
    filtered_lines = [line for line in lines if not any(word in line for word in words_to_remove)]
    # 필터링된 라인들을 다시 하나의 문자열로 결합
    return '\n'.join(filtered_lines)


# 18byte 이하인 항목 삭제
def remove_short_items(text_list: list[str], min_length=18):
    # 지정된 길이보다 긴 항목만 선택
    return [item for item in text_list if len(item) > min_length]


# 한글 문자 and 문자(\(,\))가 없는 항목 삭제
def remove_non_korean_items(text_list: list[str]):
    # 한글 문자 또는 \( 또는 \)를 포함하는 항목만 선택
    korean_pattern = re.compile('[가-힣]|\\(|\\)')
    return [item for item in text_list if korean_pattern.search(item)]
