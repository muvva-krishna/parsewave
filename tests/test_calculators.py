from app.calculators.clinical import cha2ds2_vasc, curb65


def test_cha2ds2_vasc_age_75_counts_two():
    result = cha2ds2_vasc(age=75)
    assert result["score"] == 2


def test_curb65_counts_all_five():
    result = curb65(
        confusion=True,
        bun_gt_19=True,
        respiratory_rate_gte_30=True,
        systolic_bp_lt_90=True,
        age_gte_65=True,
    )
    assert result["score"] == 5
