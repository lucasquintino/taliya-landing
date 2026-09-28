from app.domains.taliya_commercial.behavior_policy import assess_profile_name


def test_real_person_name_can_be_used_as_unverified_profile_name():
    result = assess_profile_name("Mariana Costa")

    assert result.status == "reliable"
    assert result.first_name == "Mariana"


def test_studio_brand_handle_and_phone_are_not_person_names():
    assert assess_profile_name("Studio Viva Pilates").status == "unreliable"
    assert assess_profile_name("@studio_viva").status == "unreliable"
    assert assess_profile_name("11999999999").status == "unreliable"
    assert assess_profile_name("VIVA PILATES").status == "unreliable"
