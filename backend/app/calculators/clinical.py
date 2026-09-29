def cha2ds2_vasc(*, congestive_heart_failure: bool = False, hypertension: bool = False,
                 age: int, diabetes: bool = False, stroke_tia_thromboembolism: bool = False,
                 vascular_disease: bool = False, sex_female: bool = False) -> dict:
    score = int(congestive_heart_failure) + int(hypertension)
    score += 2 if age >= 75 else 1 if 65 <= age <= 74 else 0
    score += int(diabetes) + 2 * int(stroke_tia_thromboembolism) + int(vascular_disease)
    score += int(sex_female)
    return {"score": score, "calculator": "CHA2DS2-VASc"}


def curb65(*, confusion: bool, bun_gt_19: bool, respiratory_rate_gte_30: bool,
           systolic_bp_lt_90: bool, age_gte_65: bool) -> dict:
    score = sum(map(int, [confusion, bun_gt_19, respiratory_rate_gte_30, systolic_bp_lt_90, age_gte_65]))
    return {"score": score, "calculator": "CURB-65"}


def wells_pe(*, clinical_signs_dvt: bool, pe_most_likely: bool, hr_gt_100: bool,
             immobilization_or_surgery: bool, prior_dvt_pe: bool, hemoptysis: bool,
             malignancy: bool) -> dict:
    score = 3 * int(clinical_signs_dvt) + 3 * int(pe_most_likely) + 1.5 * int(hr_gt_100)
    score += 1.5 * int(immobilization_or_surgery) + 1.5 * int(prior_dvt_pe)
    score += int(hemoptysis) + int(malignancy)
    return {"score": score, "calculator": "Wells PE"}


CALCULATORS = {
    "CHA2DS2-VASc": cha2ds2_vasc,
    "CURB-65": curb65,
    "Wells PE": wells_pe,
}
