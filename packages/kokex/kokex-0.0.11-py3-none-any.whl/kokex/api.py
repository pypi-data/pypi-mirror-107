from collections import defaultdict
from typing import Dict, List

from kokex.core.parser import DocumentParser


def keywords(docs: List[str]) -> Dict[str, int]:
    """
    문서 목록을 받아서 포함된 키워드를 리턴합니다

    :param docs: 문서 목록
    :return: 키워드와 빈도가 담긴 딕셔너리
    """
    result = defaultdict(int)
    parser = DocumentParser()

    for doc in docs:
        parser.parse(document=doc)

        for word in parser.keywords():
            result[word] += 1

    return result


def sentences(doc: str) -> List[str]:
    """
    문서를 입력 받아 문장으로 분리한 리스트를 리턴합니다

    :param doc: 문서
    :return: 문장으로 분리한 리스트
    """
    parser = DocumentParser()
    parser.parse(document=doc)

    return parser.sentences()


def parse(doc: str, debug: bool = True, custom_patterns: List[Dict[str, str]] = []):
    """
    문서를 입력받아서 파싱된 결과를 문자열로 리턴합니다

    :param doc: 입력 문서
    :param debug: true 일 경우 문서위계, 5언 7성분 9품사 정보를 함께 출력 (기본값 true)
    :param custom_patterns: 정규식 패턴과 매칭된 문자열을 위한 형태소 태그 [{'pattern': string, 'tag': string}] (기본값 [])
    :return: 출력을 위해 들여쓰기가 된 문자열
    """
    parser = DocumentParser()
    parser.parse(document=doc, custom_patterns=custom_patterns)

    return parser.printable_tree(debug=debug)
