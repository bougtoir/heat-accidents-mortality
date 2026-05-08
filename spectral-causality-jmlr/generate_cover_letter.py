#!/usr/bin/env python3
"""Generate JMLR cover letter as DOCX."""

from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from datetime import date


def build_cover_letter():
    doc = Document()

    style = doc.styles["Normal"]
    font = style.font
    font.name = "Times New Roman"
    font.size = Pt(11)

    # Sender info
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(
        "Tatsuki Onishi, MD\n"
        "Department of Anesthesiology\n"
        "University Hospital, Japan\n"
        "bougtoir@gmail.com"
    )
    run.font.size = Pt(11)

    # Date
    p = doc.add_paragraph()
    p.add_run(date.today().strftime("%B %d, %Y"))

    # Recipient
    p = doc.add_paragraph()
    p.add_run(
        "Editors\n"
        "Journal of Machine Learning Research"
    )

    # Opening
    doc.add_paragraph()
    p = doc.add_paragraph()
    p.add_run("Dear Editors,")

    # Body
    doc.add_paragraph()
    p = doc.add_paragraph()
    p.add_run(
        "I am writing to submit our manuscript entitled "
    )
    run = p.add_run(
        "\u201cSpectral Causality: Causal Direction Estimation via "
        "Magnetic Laplacians and Hodge Decomposition\u201d"
    )
    run.bold = True
    p.add_run(
        " for consideration as a regular article in the "
        "Journal of Machine Learning Research."
    )

    # Summary
    p = doc.add_paragraph()
    run = p.add_run("Summary. ")
    run.bold = True
    p.add_run(
        "This paper introduces spectral causality, a framework that "
        "estimates causal directions among observed variables by exploiting the "
        "spectral structure of the magnetic Laplacian. Unlike classical "
        "Laplacian methods, the magnetic Laplacian\u2019s complex-valued eigenvectors "
        "encode edge directionality as phase, enabling causal direction "
        "estimation from spectral structure alone. Our principal contributions are:"
    )

    # Contributions list
    contributions = [
        (
            "Directional Predictability Index (DPI)",
            " that resolves the circularity in earlier utility-based causal "
            "formulations, with partial identifiability guarantees under the "
            "additive noise model and explicit convergence rates for each component."
        ),
        (
            "Hodge-theoretic decomposition",
            " of causal edge flows into gradient (DAG-compatible), curl "
            "(feedback), and harmonic components, yielding a gradient energy "
            "ratio r_gradient that serves as a quantitative DAG-adequacy "
            "diagnostic\u2014a capability absent from existing causal discovery methods."
        ),
        (
            "Scale invariance theorem",
            " establishing that causal structure emergence depends on knowledge "
            "quality (sign pattern) rather than quantity (magnitude), together "
            "with a phase-transition analysis characterizing a U-shaped knowledge "
            "quality curve."
        ),
        (
            "Comprehensive multi-dataset validation",
            " on synthetic random DAGs (n=5\u201320, N=200\u20131000), the Sachs "
            "protein signaling network (n=11, 17 ground-truth edges), and the "
            "UCI Heart Disease dataset (n=5, N=297), benchmarked against "
            "DirectLiNGAM, the PC algorithm, GES, and NOTEARS."
        ),
    ]
    for i, (bold_part, rest) in enumerate(contributions, 1):
        p = doc.add_paragraph(style="List Number")
        run = p.add_run(bold_part)
        run.bold = True
        p.add_run(rest)

    # Relevance
    p = doc.add_paragraph()
    run = p.add_run("Relevance to JMLR. ")
    run.bold = True
    p.add_run(
        "The manuscript presents a new principled algorithm (spectral causality) "
        "grounded in spectral graph theory and Hodge theory, with sound "
        "empirical validation on both synthetic and real-world benchmarks. "
        "The theoretical analysis (17 theorem-like statements with formal proofs) "
        "advances understanding of the relationship between spectral structure "
        "and causal ordering. We believe the work is of broad interest to the "
        "machine learning community, as causal discovery is a central topic "
        "spanning methodology, theory, and applications."
    )

    # Originality
    p = doc.add_paragraph()
    run = p.add_run("Originality. ")
    run.bold = True
    p.add_run(
        "This work has not been published previously in any journal or "
        "conference proceedings. A preprint may be made available on arXiv "
        "concurrent with this submission."
    )

    # Disclosure
    p = doc.add_paragraph()
    run = p.add_run("Disclosure. ")
    run.bold = True
    p.add_run(
        "No external funding was received for this work. The author declares "
        "no conflicts of interest."
    )

    # Suggested action editors
    p = doc.add_paragraph()
    run = p.add_run("Suggested action editors. ")
    run.bold = True
    p.add_run(
        "Based on their expertise in causal discovery and spectral methods, "
        "we suggest the following action editors who may be suitable to handle "
        "this submission:"
    )

    editors = [
        ("Bernhard Sch\u00f6lkopf", "causal inference, kernel methods"),
        ("Jonas Peters", "causal discovery, additive noise models"),
        ("Peter Spirtes", "constraint-based causal discovery"),
        ("Kun Zhang", "causal discovery methodology"),
    ]
    for name, expertise in editors:
        p = doc.add_paragraph(style="List Bullet")
        run = p.add_run(name)
        run.bold = True
        p.add_run(f" \u2014 {expertise}")

    # Closing
    doc.add_paragraph()
    p = doc.add_paragraph()
    p.add_run(
        "Thank you for considering this manuscript. I look forward to receiving "
        "your editorial decision."
    )

    doc.add_paragraph()
    p = doc.add_paragraph()
    p.add_run("Sincerely,")

    doc.add_paragraph()
    p = doc.add_paragraph()
    run = p.add_run("Tatsuki Onishi, MD")
    run.bold = True
    p2 = doc.add_paragraph()
    p2.add_run(
        "Department of Anesthesiology\n"
        "University Hospital, Japan\n"
        "bougtoir@gmail.com"
    )

    out = "cover_letter.docx"
    doc.save(out)
    print(f"Cover letter generated: {out}")


if __name__ == "__main__":
    build_cover_letter()
