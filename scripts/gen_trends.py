#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
V1.5.0 热点生成器（CI 内运行，非前端）。

原则（与用户确认）：
- 热点本身必须来自真实可抓取源；绝不随机生成热点文本。
- LLM（env LLM_KEY，仅存在于 CI Secrets）只生成：whyWorthWriting / fitAccount / angle / titles，
  作用于已抓取的真实的条目；不虚构热点。无 Key 时用规则模板兜底。
- 小红书热点来自人工维护的 data/xhs-manual.json（无公开 API，禁止直抓）。
- 投资热点来自财经 RSS（不含实时行情拉取；实时行情放到未来版本）。
- 质量门 + 规模上限：today 5 / weekly 10 / ai 10 / investment 10 / xhs 5。

依赖：仅标准库（urllib / xml.etree / json / os / datetime / re / random）。
"""
import os, sys, json, re, random
from datetime import datetime, timezone, timedelta
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(DATA, "trends-daily.json")
XHS_MANUAL = os.path.join(DATA, "xhs-manual.json")

UA = {"User-Agent": "Mozilla/5.0 (compatible; pgwb-trends-bot/1.0)"}
TIMEOUT = 15

# 规模上限
CAP = {"today": 5, "weekly": 10, "ai": 10, "investment": 10, "xhs": 5, "tech": 8}

# 反套路黑名单：纯“发布/更新”无角度 → 丢弃
GENERIC_RE = re.compile(r"^(.{0,8}?(发布|更新|上线).{0,6}?(新功能|新版本|更新|v\d)|今天.{0,4}(很火|热搜))$")


def fetch(url, is_json=False, token=None):
    hdr = dict(UA)
    if token:
        hdr["Authorization"] = "Bearer " + token
    req = Request(url, headers=hdr)
    try:
        with urlopen(req, timeout=TIMEOUT) as r:
            data = r.read().decode("utf-8", "ignore")
        return json.loads(data) if is_json else data
    except (URLError, HTTPError, ValueError) as e:
        print("fetch fail:", url, "->", e)
        return None


def text_of(node):
    return (node.text or "").strip()


# ---------- 真实源抓取 ----------
def from_hn():
    out = []
    # 前台热点
    j = fetch("https://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage=30", is_json=True)
    if j:
        for h in j.get("hits", []):
            title = text_of(h.get("title") or h.get("story_title") or "")
            if not title:
                continue
            pts = h.get("points") or 0
            out.append({"cat": "tech", "hot": title, "whyHot": "Hacker News 当日 %d 分" % pts,
                        "source": "Hacker News", "url": h.get("url") or ("https://news.ycombinator.com/item?id=" + str(h.get("objectID", ""))),
                        "summary": "", "metric": pts})
    # AI 相关
    j2 = fetch("https://hn.algolia.com/api/v1/search_by_date?tags=story&query=AI&hitsPerPage=20", is_json=True)
    if j2:
        for h in j2.get("hits", []):
            title = text_of(h.get("title") or h.get("story_title") or "")
            if not title:
                continue
            pts = h.get("points") or 0
            out.append({"cat": "ai", "hot": title, "whyHot": "Hacker News %d 分" % pts,
                        "source": "Hacker News", "url": h.get("url") or "", "summary": "", "metric": pts})
    return out


def from_arxiv():
    out = []
    for cat in ["cs.AI", "cs.CL", "cs.LG"]:
        xml = fetch("https://rss.arxiv.org/rss/%s" % cat)
        if not xml:
            continue
        try:
            root = ET.fromstring(xml)
        except ET.ParseError:
            continue
        for item in root.iter("item"):
            title = text_of(item.find("title"))
            if not title:
                continue
            link = text_of(item.find("link"))
            desc = text_of(item.find("description"))
            out.append({"cat": "ai", "hot": title.split(" (")[0].strip(),
                        "whyHot": "arXiv %s 新论文" % cat,
                        "source": "arXiv/%s" % cat, "url": link, "summary": desc[:120], "metric": 40})
    return out


def from_github(token):
    out = []
    url = "https://api.github.com/search/repositories?q=AI+created:%3E2024-01-01&sort=stars&order=desc&per_page=15"
    j = fetch(url, is_json=True, token=token)
    if j:
        for r in j.get("items", []):
            out.append({"cat": "ai", "hot": "GitHub 热门项目：" + text_of(r.get("full_name") or ""),
                        "whyHot": "本周 %d 星" % (r.get("stargazers_count") or 0),
                        "source": "GitHub", "url": r.get("html_url") or "", "summary": text_of(r.get("description") or ""),
                        "metric": (r.get("stargazers_count") or 0)})
    return out


def from_rss_feeds(urls, cat):
    out = []
    for u in urls:
        xml = fetch(u)
        if not xml:
            continue
        try:
            root = ET.fromstring(xml)
        except ET.ParseError:
            continue
        for item in root.iter("item"):
            title = text_of(item.find("title"))
            if not title:
                continue
            link = text_of(item.find("link"))
            pub = text_of(item.find("pubDate"))
            out.append({"cat": cat, "hot": title, "whyHot": "科技媒体新动态",
                        "source": u.split("/")[2], "url": link, "summary": "", "metric": 55, "date": pub})
    return out


def from_finance_rss():
    urls = [
        "https://www.cnbc.com/id/10000664/device/rss/rss.html",
        "https://feeds.content.dowjones.io/public/rss/mktw_topstories",
    ]
    return from_rss_feeds(urls, "investment")


def from_tech_rss():
    urls = [
        "https://techcrunch.com/feed/",
        "https://www.theverge.com/rss/index.xml",
        "https://dev.to/feed",
    ]
    return from_rss_feeds(urls, "tech")


# ---------- 评分 ----------
def score_of(it):
    m = it.get("metric") or 0
    cat = it.get("cat")
    try:
        if cat == "ai" and it.get("source") == "GitHub":
            return int(min(95, 60 + m / 1000.0))
        if it.get("source") == "Hacker News":
            return int(min(95, 60 + m / 12.0))
        if cat == "investment":
            return int(min(85, 60 + random.randint(0, 25)))
        return int(min(85, 62 + random.randint(0, 20)))
    except Exception:
        return 70


# ---------- LLM 仅生成衍生字段 ----------
def llm_enrich(it, key, base):
    if not key:
        return rule_enrich(it)
    prompt = (
        "你是内容策划。基于下面这条真实热点，只输出 JSON："
        "{\"whyWorthWriting\":\"为什么值得写成内容(对创作/投资/工作哪类人有用)\","
        "\"fitAccount\":\"适合什么类型账号\",\"angle\":\"推荐切入点(真实问题→我的选择→行动→结果→复盘)\","
        "\"titles\":[\"标题1\",\"标题2\",\"标题3\"]}。不要虚构热点，不要解释。\n热点：%s\n来源：%s"
        % (it.get("hot", ""), it.get("source", ""))
    )
    try:
        body = json.dumps({"model": os.environ.get("LLM_MODEL", "gpt-4o-mini"), "messages": [{"role": "user", "content": prompt}],
                           "temperature": 0.4, "response_format": {"type": "json_object"}}).encode("utf-8")
        req = Request((base or "https://api.openai.com/v1") + "/chat/completions", data=body,
                      headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
        with urlopen(req, timeout=TIMEOUT) as r:
            j = json.loads(r.read().decode("utf-8", "ignore"))
        txt = j["choices"][0]["message"]["content"]
        d = json.loads(txt)
        return {"whyWorthWriting": d.get("whyWorthWriting", ""), "fitAccount": d.get("fitAccount", ""),
                "angle": d.get("angle", ""), "titles": d.get("titles", [])}
    except Exception as e:
        print("llm fail, fallback:", e)
        return rule_enrich(it)


def rule_enrich(it):
    cat = it.get("cat")
    if cat == "investment":
        return {"whyWorthWriting": "帮普通人理解市场变化并做决策", "fitAccount": "投资理财号",
                "angle": "用真实数字和我的配置讲清这件事", "titles": [it.get("hot", ""), it.get("hot", "") + "怎么看", "普通人该怎么做"]}
    if cat == "xhs":
        return {"whyWorthWriting": "真实经历最有共鸣", "fitAccount": "自媒体号 / 女性成长号",
                "angle": "用我自己的故事切入", "titles": [it.get("hot", ""), it.get("hot", "") + "的坑", "我是怎么做的"]}
    return {"whyWorthWriting": "真实技术趋势，对创作者/职场人有用", "fitAccount": "AI工具号 / 独立开发号",
            "angle": "我亲测/观察后的真实切入点", "titles": [it.get("hot", ""), "我怎么用上" + it.get("hot", ""), "普通人能从中得到什么"]}


# ---------- 质量门 ----------
def passes_gate(it):
    hot = (it.get("hot") or "").strip()
    if len(hot) < 4:
        return False
    if not it.get("source"):
        return False
    if GENERIC_RE.search(hot):
        return False
    return True


def value_tag(cat):
    return {"ai": ["creation", "work"], "tech": ["creation", "work"],
            "investment": ["investment"], "xhs": ["creation"]}.get(cat, ["creation"])


# ---------- 主题去重（连续 7 天窗口，避免同主题霸榜） ----------
THEME_BRANDS = ["openai", "chatgpt", "gpt-4", "gpt-5", "gpt", "anthropic", "claude", "gemini",
    "google", "meta ai", "meta", "llama", "mistral", "deepseek", "xai", "grok", "copilot", "cursor",
    "github", "apple", "tesla", "nvidia", "微软", "谷歌", "阿里", "通义", "千问", "百度", "文心",
    "腾讯", "字节", "小红书", "抖音", "微信", "b站", "雪球", "比特币", "ethereum", "eth", "solana"]
HISTORY = os.path.join(DATA, "trends-history.json")
WINDOW_DAYS = 7

def theme_key(hot):
    """去重依据：命中已知品牌/实体词则用该词，否则取热点文本前 6 个有效字符。"""
    s = (hot or "").lower()
    for b in THEME_BRANDS:
        if b in s:
            return b
    m = re.sub(r"[^a-z0-9一-龥]", "", s)[:6]
    return m or "misc"

def load_history():
    try:
        with open(HISTORY, encoding="utf-8") as f:
            d = json.load(f)
        if isinstance(d, dict) and isinstance(d.get("days"), list):
            return d["days"]
    except Exception:
        pass
    return []

def prune_history(days):
    cutoff = (datetime.now(timezone(timedelta(hours=8))) - timedelta(days=WINDOW_DAYS)).strftime("%Y-%m-%d")
    # 严格大于 cutoff => 仅保留最近 7 天（今天-6 .. 今天）
    return [d for d in days if d.get("date", "") > cutoff]

def save_history(days):
    with open(HISTORY, "w", encoding="utf-8") as f:
        json.dump({"days": prune_history(days)}, f, ensure_ascii=False, indent=2)

def cross_day_adjust(items, history, today_str):
    """跨天降权：统计最近 7 天（不含今天）各主题出现次数；≥3 次直接剔除，≥1 次按次数降权。"""
    counts = {}
    for d in history:
        if d.get("date") == today_str:
            continue
        for th in d.get("themes", []):
            counts[th] = counts.get(th, 0) + 1
    out = []
    for it in items:
        th = theme_key(it["hot"])
        c = counts.get(th, 0)
        if c >= 3:
            continue
        if c >= 1:
            it["trendScore"] = max(45, int(it["trendScore"]) - 8 * c)
        out.append(it)
    return out

def same_day_dedup(items):
    """同日同主题仅保留 trendScore 最高的一条，其余剔除（保证当日主题多样性）。"""
    best = {}
    for it in items:
        key = (it.get("cat"), theme_key(it["hot"]))
        if key not in best or it["trendScore"] > best[key]["trendScore"]:
            best[key] = it
    return list(best.values())


def main():
    token = os.environ.get("GITHUB_TOKEN")
    llm_key = os.environ.get("LLM_KEY")
    llm_base = os.environ.get("LLM_BASE")

    raw = []
    raw += from_hn()
    raw += from_arxiv()
    raw += from_github(token)
    raw += from_tech_rss()
    raw += from_finance_rss()

    # 去重（按 hot 归一）
    seen = set()
    items = []
    for it in raw:
        if not passes_gate(it):
            continue
        k = it["hot"].lower()
        if k in seen:
            continue
        seen.add(k)
        it["trendScore"] = score_of(it)
        items.append(it)

    # 小红书：人工维护
    try:
        with open(XHS_MANUAL, encoding="utf-8") as f:
            xhs = json.load(f)
        for x in xhs:
            x["sourceType"] = "manual"
            if "trendScore" not in x:
                x["trendScore"] = 72
            items.append(x)
    except Exception as e:
        print("xhs manual load fail:", e)

    # LLM / 规则 生成衍生字段
    for it in items:
        en = llm_enrich(it, llm_key, llm_base)
        it["whyWorthWriting"] = en.get("whyWorthWriting", "")
        it["fitAccount"] = en.get("fitAccount", "")
        it["angle"] = en.get("angle", "")
        it["titles"] = en.get("titles", [it.get("hot", "")])
        it["valueTag"] = value_tag(it.get("cat"))
        it["date"] = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d")
        it.setdefault("sourceType", "scrape")
        it.setdefault("summary", it.get("summary", ""))
        # 清理内部字段
        it.pop("metric", None)

    # 主题去重（连续 7 天窗口）：先跨天降权/剔除，再同日同主题去重
    today_str = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d")
    history = load_history()
    items = cross_day_adjust(items, history, today_str)
    items = same_day_dedup(items)

    items.sort(key=lambda x: x.get("trendScore", 0), reverse=True)

    def top(cat, n):
        pool = [x for x in items if x.get("cat") == cat]
        return pool[:n]

    final = []
    final += top("ai", CAP["ai"])
    final += top("investment", CAP["investment"])
    final += top("xhs", CAP["xhs"])
    final += top("tech", CAP["tech"])
    # 去重（tech 可能与 ai 重叠极少）
    ids = set()
    final = [x for x in final if not (x["id"] in ids or ids.add(x.get("id", x["hot"])))]
    final.sort(key=lambda x: x.get("trendScore", 0), reverse=True)

    doc = {
        "generatedAt": datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "source": "CI+manual",
        "trends": final,
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
    # 更新滚动 7 天主题历史（仅记录今日发布的主题，供次日跨天降权使用）
    published_themes = [theme_key(x["hot"]) for x in final]
    history.append({"date": today_str, "themes": published_themes})
    save_history(history)
    print("generated", len(final), "trends (ai=%d tech=%d inv=%d xhs=%d)" % (
        sum(1 for x in final if x["cat"] == "ai"),
        sum(1 for x in final if x["cat"] == "tech"),
        sum(1 for x in final if x["cat"] == "investment"),
        sum(1 for x in final if x["cat"] == "xhs")))


if __name__ == "__main__":
    main()
