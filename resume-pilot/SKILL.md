---
name: resume-pilot
description: Customizes a resume for a target job description by iteratively rewriting bullet content to match keywords that is ATS-friendly, while preserving the original PDF/DOCX resume structure, layout, and headers.
---

# Resume Pilot Skill

## What this skill does
- Accepts an input resume file in `.doc`, `.docx`, or `.pdf` format.
- Accepts a job description prompt or text input.
- Iterates on the job description to customize resume bullets to fit the target role.
- Produces a final output resume in `.pdf` format.
- Preserves the original resume formatting, section order, and headers.
- Only bullet content may be modified, with the case of certain exceptions; headers and section titles must remain unchanged.

## Workflow
1. Receive the original resume file and target job description, and make sure to follow guardrails and quality criteria while following the entire workflow.
2. Extract the resume structure from [template][template.pdf] identifying headers, sections, and bullet lists.
3. Analyze the job description for relevant keywords, responsibilities, and required skills.
4. Rewrite each bullet so it aligns with the job description keywords and emphasizes relevant experience.
5. Keep all original headers, section titles, and document structure intact.
6. Export the customized resume back to a PDF that retains the original layout and formatting.
7. Verify the output preserves the original resume's structure and only changes bullet text.

## Quality criteria
- Output is a valid `.pdf` resume.
- The original resume headers and section titles remain unchanged.
- Section order and document structure are preserved.
- Bullets are rewritten to better match the target job description. Has to be ATS-friendly and include relevant keywords.
- Formatting, spacing, and visual layout remains the same as the source resume.
- No new sections are added or removed.

## Guardrails
- Do not modify any text outside of bullet points.
- Do not change the order of sections or headers.
- Keep the resume to 1 page if the original was 1 page, or 2 pages if the original was 2 pages.
- Ensure the final output is a PDF file, regardless of input format.
- Spacing and formatting must be preserved to maintain the original resume's visual design - this should be an exact match in terms of layout, fonts, and spacing. Every aspect of the original formatting should be retained, except for the content of the bullet points.

## Exceptions
- If the original resume contains a "Summary" or "Objective" section, you may modify the text in that section to better align with the job description, but you must not change the section header.
- If the original resume contains a "Skills" section, you may modify the bullet points in that section to better match the job description keywords, has to be ATS-friendly

## Example prompts to try
- "Customize my attached resume for this job description, keeping the original PDF format and only editing bullet content."
- "Use the job description keywords to tailor my resume bullets, and return a PDF that preserves headers and structure."
- "Iterate on the attached resume and job description to create a customized PDF resume with the same layout and section titles."
