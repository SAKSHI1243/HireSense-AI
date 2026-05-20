def generate_recruiter_summary(
    score,
    skills,
    missing_skills
):

    strengths = ", ".join(skills[:5])

    missing = ", ".join(missing_skills[:3])

    if score >= 80:

        return f"""
        Candidate demonstrates strong alignment
        with the job requirements.

        Key strengths include:
        {strengths}.

        Suitable for advanced ML/NLP-focused roles.
        """

    elif score >= 60:

        return f"""
        Candidate shows moderate compatibility
        with the target role.

        Strong areas:
        {strengths}.

        Improvement recommended in:
        {missing}.
        """

    else:

        return f"""
        Candidate profile currently lacks
        strong alignment with the role.

        Missing areas include:
        {missing}.
        """