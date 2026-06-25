from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)


def generate_report(
    filename,
    career,
    score,
    feedback,
    missing_skills,
    top_jobs
):

    doc = SimpleDocTemplate(
        filename
    )

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "Resume Analysis Report",
            styles["Title"]
        )
    )
    content.append(
        Paragraph(
            f"Resume Feedback: {feedback}",
            styles["Normal"]
        )
    )

    content.append(
        Spacer(1, 20)
    )

    content.append(
        Paragraph(
            f"Career Recommendation: {career}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Resume Score: {score}",
            styles["Normal"]
        )
    )

    content.append(
        Spacer(1, 10)
    )

    content.append(
        Paragraph(
            "Missing Skills",
            styles["Heading2"]
        )
    )

    for skill in missing_skills:

        content.append(
            Paragraph(
                f"• {skill}",
                styles["Normal"]
            )
        )
    content.append(
        Spacer(1, 15)
    )

    content.append(
        Paragraph(
            "Top Matching Jobs",
            styles["Heading2"]
        )
    )

    for _, row in top_jobs.head(5).iterrows():

        content.append(
            Paragraph(
                f"{row['JobTitle']} - {row['Company']}",
                styles["Normal"]
            )
        )

    doc.build(content)
