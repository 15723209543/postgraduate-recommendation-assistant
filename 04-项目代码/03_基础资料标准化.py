import re


def clean(value):
    return str(value or "").strip()


def find_first(text, patterns):
    for pattern in patterns:
        m = re.search(pattern, text, re.I)
        if m:
            return clean(m.group(1)).replace("**", "").strip()
    return ""


def to_int(value):
    m = re.search(r"\d+", str(value or ""))
    return int(m.group()) if m else None


def main(student_data):
    text = clean(student_data)

    school_name = find_first(text, [
        r"学校官方全称[：:]\s*([^\n\r]+)",
        r"学校名称[：:]\s*([^\n\r]+)",
        r"学校[：:]\s*([^\n\r]+)"
    ])
    major_name = find_first(text, [
        r"专业全称[：:]\s*([^\n\r]+)",
        r"专业名称[：:]\s*([^\n\r]+)",
        r"专业[：:]\s*([^\n\r]+)"
    ])
    grade = find_first(text, [r"学生年级[：:]\s*([^\n\r]+)", r"年级[：:]\s*([^\n\r]+)"])
    rank_raw = find_first(text, [r"当前专业排名[：:]\s*([^\n\r]+)", r"专业排名[：:]\s*([^\n\r]+)"])
    total_raw = find_first(text, [r"专业总人数[：:]\s*([^\n\r]+)", r"总人数[：:]\s*([^\n\r]+)"])

    # 兼容 64/400
    frac = re.search(r"(?<!\d)(\d+)\s*/\s*(\d+)(?!\d)", text)
    rank = to_int(rank_raw)
    total = to_int(total_raw)
    if frac:
        if rank is None:
            rank = int(frac.group(1))
        if total is None:
            total = int(frac.group(2))

    missing = []
    if not grade: missing.append("学生年级")
    if not school_name: missing.append("学校")
    if not major_name: missing.append("专业")
    if rank is None: missing.append("专业排名")
    if total is None: missing.append("专业总人数")

    valid = not missing
    error = ""
    if rank is not None and rank <= 0:
        valid = False; error = "专业排名必须为正整数"
    elif total is not None and total <= 0:
        valid = False; error = "专业总人数必须为正整数"
    elif rank is not None and total is not None and rank > total:
        valid = False; error = "专业排名不能大于专业总人数"
    elif missing:
        error = "缺少必要信息：" + "、".join(missing)

    rank_ratio = round(rank / total * 100, 2) if rank and total and rank <= total else None

    return {
        "student_data": text,
        "school_name": school_name,
        "major_name": major_name,
        "grade": grade,
        "rank": rank if rank is not None else 0,
        "total": total if total is not None else 0,
        "rank_ratio": rank_ratio if rank_ratio is not None else 0.0,
        "data_valid": bool(valid),
        "error": error
    }
