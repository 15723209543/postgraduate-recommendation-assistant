import re


def clean_text(value):
    return str(value or "").strip()


def extract_field(text, labels):
    for label in labels:
        pattern = rf"(?:^|\n)\s*{re.escape(label)}\s*[：:]\s*([^\n\r]+)"
        m = re.search(pattern, text, re.I)
        if m:
            return clean_text(m.group(1)).replace("**", "").strip()
    return ""


def main(student_data):
    text = clean_text(student_data)

    school_name = extract_field(text, ["学校官方全称", "学校名称", "学校"])
    major_name = extract_field(text, ["专业全称", "专业名称", "专业"])

    # 兼容“学校、大二、64/400、专业”一类简写输入
    if not school_name or not major_name:
        parts = [p.strip() for p in re.split(r"[,，;；]", text) if p.strip()]
        if not school_name and parts:
            school_name = parts[0]
        if not major_name:
            for p in reversed(parts):
                if re.search(r"(工程|科学|技术|医学|法学|经济|管理|文学|教育|数学|物理|化学|材料|自动化|电子|计算机|人工智能)", p):
                    major_name = p
                    break

    queries = []
    if school_name:
        queries.extend([
            f'{school_name} 推荐优秀应届本科毕业生免试攻读研究生 推免 工作办法 官方',
            f'{school_name} 推免 名额 拟推荐名单 本科 官方',
            f'{school_name} 教务处 推免 2026 2027 官方'
        ])
    if school_name and major_name:
        queries.extend([
            f'{school_name} {major_name} 推免 实施细则 学院 官方',
            f'{school_name} {major_name} 培养方案 本科 官方',
            f'{school_name} {major_name} 推免 名单 名额 历年 官方'
        ])

    output = "\n".join(queries)
    return {
        "school_name": school_name,
        "major_name": major_name,
        "output": output
    }
