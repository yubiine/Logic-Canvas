import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR / "src"))

from logic_canvas.exam_seed import EXAM_TOPICS, seed_exam_topics


def main() -> None:
    inserted = seed_exam_topics()
    print("성공! 총 {}개의 핵심 정처기 개념 시드가 준비되어 있습니다.".format(len(EXAM_TOPICS)))
    print("이번 실행에서 반영된 행 수: {}".format(inserted))
    print("웹 페이지를 새로고침해서 확인하세요.")


if __name__ == "__main__":
    main()
