#!/usr/bin/env python3
"""ETF 사이트 모든 페이지에 JSON-LD 구조화 데이터 자동 삽입"""
import json, re, os

BASE = "/root/etf-simulator"
DOMAIN = "https://etfsimulator.blog"
DATE_MODIFIED = "2026-06-22"

def generate_website_schema():
    return {
        "@context": "https://schema.org", "@type": "WebSite",
        "name": "ETF 적립식 투자 시뮬레이터", "url": DOMAIN,
        "description": "SPY·QQQ·SCHD 등 10종 ETF의 20년 장기 수익률과 ISA·IRP·연금저축 세금 혜택을 무료로 비교하는 교육용 시뮬레이터",
        "potentialAction": {"@type": "SearchAction", "target": {"@type": "EntryPoint", "urlTemplate": f"{DOMAIN}/?q={{search_term_string}}"}, "query-input": "required name=search_term_string"}
    }

def generate_organization_schema():
    return {"@context": "https://schema.org", "@type": "Organization", "name": "ETF 적립식 투자 시뮬레이터", "url": DOMAIN}

def generate_faq_schema():
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": "ETF가 뭔가요? 일반 주식이랑 뭐가 다른가요?", "acceptedAnswer": {"@type": "Answer", "text": "ETF(Exchange Traded Fund)는 S&P500이나 나스닥100 같은 지수를 그대로 따라가는 펀드입니다. 개별 주식을 고를 필요 없이, ETF 하나만 사면 수백 개 기업에 분산투자하는 효과를 얻을 수 있어요."}},
        {"@type": "Question", "name": "ISA, IRP, 연금저축 중에 뭐가 제일 좋나요?", "acceptedAnswer": {"@type": "Answer", "text": "ISA는 3년 만기, 중도인출 자유, 200만원 비과세로 단기·중기에 적합합니다. IRP/연금저축은 55세까지 묶는 대신 세액공제와 과세이연 효과로 장기 노후자금에 유리합니다."}},
        {"@type": "Question", "name": "이 시뮬레이터의 수익률은 정확한가요?", "acceptedAnswer": {"@type": "Answer", "text": "아니요. 이 시뮬레이터는 과거 평균 수익률과 배당률을 바탕으로 한 교육 목적의 가상 시뮬레이션입니다. 실제 투자 수익은 시장 상황에 따라 크게 달라질 수 있으며, 원금 손실 가능성도 있습니다."}},
        {"@type": "Question", "name": "해외 ETF에 투자할 때 세금은 어떻게 되나요?", "acceptedAnswer": {"@type": "Answer", "text": "배당소득은 15.4% 원천징수(ISA 계좌 시 200만원까지 비과세), 매도차익은 연 250만원 초과 시 22% 양도소득세가 부과됩니다. ISA 계좌 적극 활용을 권장합니다."}},
    ]}

def generate_breadcrumb(path_parts):
    items = [{"@type": "ListItem", "position": 1, "name": "홈", "item": DOMAIN}]
    url = DOMAIN
    for i, (name, slug) in enumerate(path_parts, start=2):
        url += f"/{slug}"
        items.append({"@type": "ListItem", "position": i, "name": name, "item": url})
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}

def generate_blogposting(url, title, desc, category):
    return {"@context": "https://schema.org", "@type": "BlogPosting", "headline": title, "description": desc,
            "url": url, "datePublished": DATE_MODIFIED, "dateModified": DATE_MODIFIED,
            "author": {"@type": "Person", "name": "김정환"},
            "publisher": {"@type": "Organization", "name": "ETF 적립식 투자 시뮬레이터"},
            "articleSection": category, "inLanguage": "ko-KR", "isAccessibleForFree": True,
            "mainEntityOfPage": {"@type": "WebPage", "@id": url}}

def insert_jsonld(html, schemas):
    blocks = "\n".join(f'<script type="application/ld+json">\n{json.dumps(s, ensure_ascii=False, indent=2)}\n</script>' for s in schemas)
    return html.replace('</head>', f'{blocks}\n</head>', 1)

blog_posts = [
    ("etf-beginner-guide.html", "ETF 투자, 이것만 알면 시작할 수 있다 — 2026 완벽 입문 가이드", "ETF가 뭔지 모르겠다면 이 글 하나로 끝내세요.", "기초"),
    ("isa-vs-irp.html", "ISA vs IRP vs 연금저축 — 내 돈에 맞는 절세 계좌는?", "비과세, 세액공제, 과세이연의 장단점을 실제 데이터로 비교합니다.", "절세"),
    ("monthly-investing.html", "월 50만원으로 20년 적립식 — 복리의 마법, 숫자로 증명하기", "S&P500 ETF 월 적립식 20년 시뮬레이션 결과.", "전략"),
    ("etf-comparison.html", "SPY vs QQQ vs SCHD — 대표 ETF 3종 10년 수익률 완벽 비교", "과거 10년 수익률·배당률·변동성 분석.", "비교"),
    ("isa-account-guide.html", "2026년 ISA 계좌 개설 방법 A to Z — 5분 만에 뚝딱", "증권사 선택부터 개설, ETF 매수까지 단계별 안내.", "가이드"),
    ("etf-mistakes.html", "ETF 투자할 때 가장 흔한 실수 7가지 — 꼭 피해야 할 함정", "분산투자 착각, 잦은 매매, 배당률 함정 등 해결책.", "주의"),
    ("dividend-1m.html", "배당 ETF로 월 100만원 받으려면 얼마 필요할까?", "고배당 ETF로 목표 배당금을 위한 현실적 투자금 계산.", "배당"),
    ("office-worker-portfolio.html", "직장인을 위한 3단계 ETF 포트폴리오 — 나이별 추천", "20대~50대별 최적 조합, 바쁜 직장인용 전략.", "포트폴리오"),
    ("pension-vs-irp.html", "연금저축 vs IRP 10년 시뮬레이션 — 세금까지 비교", "월 30만원 10년 투자 시 실제 수익·세금 데이터 비교.", "연금"),
    ("overseas-etf-tax.html", "해외 ETF 세금 완벽 정리 — 양도세·배당세·ISA까지", "SPY·QQQ·SCHD 투자 시 배당세·양도세·미국 원천징수세 총망라.", "세금"),
    ("dca-reality.html", "매달 50만원씩 ETF 5년 모은 후기", "55개월 실제 적립식 투자 데이터 공개 및 장단점 분석.", "후기"),
    ("recession-strategy.html", "경기침체 올 때 ETF로 대처하는 법", "2008·2020·2022년 하락장 데이터 기반 생존 전략.", "전략"),
]

etf_pages = [
    ("spy.html", "SPY ETF — 미국 주식시장 그 자체", "S&P500 추종, 30년 역사, 초보자·전문가 모두 선호하는 ETF 완벽 분석."),
    ("qqq.html", "QQQ ETF — 기술주의 미래에 베팅", "나스닥100 추종, 연 17.8% 수익률, 고변동성 ETF 심층 분석."),
    ("schd.html", "SCHD ETF — 배당주 투자의 정석", "연 3.8% 배당, 낮은 변동성, 배당 재투자 복리 효과 분석."),
    ("vt.html", "VT ETF — 지구 전체에 투자한다는 것", "50개국 9,000개 종목, 진정한 글로벌 분산투자 ETF 분석."),
    ("tiger-sp500.html", "TIGER S&P500 — 환전 없이 SPY 투자", "원화로 S&P500 투자, ISA 계좌 활용 이점, 환율 리스크 분석."),
]

results = []

# 1. index.html
with open(f"{BASE}/index.html") as f:
    html = f.read()
schemas = [generate_website_schema(), generate_organization_schema(), generate_faq_schema(), generate_breadcrumb([])]
html = insert_jsonld(html, schemas)
with open(f"{BASE}/index.html", 'w') as f:
    f.write(html)
results.append("✅ index.html (WebSite+Organization+FAQ+Breadcrumb)")

# 2. Blog posts
for fn, title, desc, cat in blog_posts:
    with open(f"{BASE}/blog/{fn}") as f:
        html = f.read()
    url = f"{DOMAIN}/blog/{fn}"
    schemas = [generate_blogposting(url, title, desc, cat), generate_breadcrumb([("블로그", "blog"), (cat, f"blog/{fn}")])]
    html = insert_jsonld(html, schemas)
    with open(f"{BASE}/blog/{fn}", 'w') as f:
        f.write(html)
    results.append(f"✅ blog/{fn}")

# 3. ETF pages
for fn, title, desc in etf_pages:
    with open(f"{BASE}/etf/{fn}") as f:
        html = f.read()
    url = f"{DOMAIN}/etf/{fn}"
    schemas = [generate_blogposting(url, title, desc, "ETF 분석"), generate_breadcrumb([("ETF 상세", "etf"), (title.split("—")[0].strip(), f"etf/{fn}")])]
    html = insert_jsonld(html, schemas)
    with open(f"{BASE}/etf/{fn}", 'w') as f:
        f.write(html)
    results.append(f"✅ etf/{fn}")

# 4. Static pages
for fn in ["about.html", "privacy.html", "glossary.html", "brokerages.html"]:
    with open(f"{BASE}/{fn}") as f:
        html = f.read()
    schemas = [{"@context": "https://schema.org", "@type": "WebPage", "name": fn.replace(".html","").capitalize(), "url": f"{DOMAIN}/{fn}"}, generate_breadcrumb([(fn.replace(".html",""), fn)])]
    html = insert_jsonld(html, schemas)
    with open(f"{BASE}/{fn}", 'w') as f:
        f.write(html)
    results.append(f"✅ {fn}")

for r in results:
    print(r)
print(f"\n총 {len(results)}개 페이지 JSON-LD 삽입 완료!")
