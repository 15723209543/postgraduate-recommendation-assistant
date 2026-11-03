import re


def clean(value):
    value = str(value or "").strip()
    value = re.sub(r"^[\s•·\-*#]+", "", value)
    return value.strip()


def extract_school_name(text):
    patterns = [
        r"学校官方全称[：:]\s*([^\n\r]+)",
        r"官方全称[：:]\s*([^\n\r]+)",
        r"学校名称[：:]\s*([^\n\r]+)"
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            name = clean(match.group(1)).replace("**", "").strip()
            if name:
                return name
    return ""


def check_school_real(text):
    positive_patterns = [
        r"学校真实性核验[：:]\s*(通过|真实|是|已通过|确认通过)",
        r"学校真实性[：:]\s*(通过|真实|是|已确认)",
        r"确认.*?为.*?大学",
        r"确认.*?为.*?高校",
        r"真实存在.*?高校",
        r"真实存在.*?大学",
        r"教育部直属",
        r"全国重点大学",
        r"985",
        r"211",
        r"双一流"
    ]
    return any(re.search(p, text, re.I) for p in positive_patterns)


def check_push_qualification(text):
    positive_patterns = [
        r"学校推免资格[：:]\s*(具有|具备|是|有|通过|已确认)",
        r"推免资格[：:]\s*(具有|具备|是|有|通过|已确认)",
        r"具有推荐优秀应届本科毕业生免试",
        r"具备推荐优秀应届本科毕业生免试",
        r"具有.*?推荐免试.*?资格",
        r"具备.*?推荐免试.*?资格",
        r"具有本科推免资格",
        r"具备本科推免资格",
        r"具有明确的本科推免资格",
        r"具有合法推免资格"
    ]
    return any(re.search(p, text, re.I) for p in positive_patterns)


def check_explicit_failure(text):
    failure_patterns = [
        r"学校真实性核验[：:]\s*(未通过|失败|无法确认|无法核验)",
        r"学校真实性[：:]\s*(未通过|失败|无法确认|无法核验)",
        r"学校推免资格[：:]\s*(不具有|不具备|没有|无|未通过)",
        r"不具有.*?推免资格",
        r"不具备.*?推免资格",
        r"无法确认.*?学校.*?真实存在",
        r"无法确认.*?具有.*?推免资格",
        r"不是.*?本科高校"
    ]
    return any(re.search(p, text, re.I) for p in failure_patterns)


def main(verification_text):
    text = str(verification_text or "").strip()
    verification = text
    school_name = extract_school_name(text)
    school_real = check_school_real(text)
    push_qualified = check_push_qualification(text)
    explicit_failure = check_explicit_failure(text)

    # 学院归属、专业细则、专业推免率等后续信息缺失，不参与学校资格失败判断。
    school_verified = bool(school_real and push_qualified and not explicit_failure)

    return {
        "verification": verification,
        "school_verified": school_verified,
        "school_name": school_name
    }
