"""후기 캡처 리사이즈: 가로 900px 이하, JPEG q80. 멱등(재실행해도 재크롭·재축소 없음).
usage: python tools/resize_reviews.py [quality]
"""
import glob, os, sys
from PIL import Image

ROOT = os.path.join(os.path.dirname(__file__), '..', 'assets', 'reviews')
MAX_W = 900
Q = int(sys.argv[1]) if len(sys.argv) > 1 else 80
# 파일명 -> (원본 높이, 유지할 y 시작). 원본 높이일 때만 크롭(멱등).
CROP = {
    '구매후기5.jpg': (681, 316),   # "8,900원" 줄 포함 상단 5줄 제거
    '수업후기30.jpg': (1137, 825), # 상단 일정 상담 대화 제거, 후기 말풍선만
}

total = 0
for f in sorted(glob.glob(os.path.join(ROOT, '*', '*.jpg'))):
    im = Image.open(f).convert('RGB')
    name = os.path.basename(f)
    if name in CROP and im.height == CROP[name][0]:
        im = im.crop((0, CROP[name][1], im.width, im.height))
    if im.width > MAX_W:
        im = im.resize((MAX_W, round(im.height * MAX_W / im.width)), Image.LANCZOS)
    im.save(f, 'JPEG', quality=Q, optimize=True)
    sz = os.path.getsize(f)
    total += sz
    print(f'{name:16s} {im.width}x{im.height} {sz//1024:4d}KB')
print(f'TOTAL {total/1024:.0f}KB ({total/1024/1024:.2f}MB)')
assert total < 2 * 1024 * 1024, 'over 2MB — rerun with lower quality'
