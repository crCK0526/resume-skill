# Evidence and Copy Guide

## Evidence hierarchy

Evaluate evidence by relevance to the exact claim, not by visual formality alone.

| Evidence | Usually confirms | Does not automatically confirm |
|---|---|---|
| Identity/basic-info form supplied by user | Name, contact, target role, stated school | Accuracy against government records |
| Graduation/enrollment record | Institution, major, dates, degree | Unrelated awards or duties |
| Award certificate | Award name, level, date, organizers, named recipients | Candidate's exact contribution unless stated |
| Student cadre record | Role, class/organization, listed term | Quantified performance |
| Training certificate | Training name, recognition, date, issuer | Employment experience |
| Employment proof | Employer, role, dates, sometimes duties | Unlisted metrics or responsibilities |
| Portfolio artifact | Existence and visible output | Full ownership unless authorship is established |

A certificate issued by Institution B does not by itself contradict a stated graduation school of Institution A. Flag the mismatch for confirmation only when it materially affects the resume.

## Fact-ledger JSON schema

Use an array of objects:

```json
[
  {
    "category": "award",
    "claim": "Won third prize in a provincial vocational skills competition",
    "source": "award_photo_01.jpg, main body",
    "confidence": "high",
    "status": "confirmed",
    "note": "Candidate name and award level are visible"
  }
]
```

Allowed `confidence` values:

- `high`: Explicit, legible, and directly relevant evidence
- `medium`: Partially legible or indirectly supported
- `low`: Inference, ambiguous text, or uncertain ownership

Allowed `status` values:

- `confirmed`: Safe to use as stated
- `conflict`: Contradictory evidence exists
- `missing`: Required data is absent
- `derived`: Reasonable wording derived from confirmed facts; label internally
- `excluded`: Deliberately omitted

Allowed `category` values:

- `basic_info`
- `education`
- `work`
- `campus`
- `award`
- `certificate`
- `skill`
- `project`

## Blocking conditions

Treat the following as blockers for a final resume unless the user explicitly accepts a placeholder:

- Candidate name unknown
- Target role unknown when role-specific optimization was requested
- Directly conflicting school, employer, role, or date information
- Employment entry without a usable time range
- Award assigned to the candidate when the candidate's name is not visible or otherwise confirmed
- A claimed metric without an auditable source

## Copy rules

### Work and project bullets

Preferred pattern:

`Action + object/scope + method + output/result`

Examples:

- `负责门店短视频账号的选题、拍摄与剪辑，形成稳定的周更内容流程。`
- `参与融媒体赛项的选题策划与内容制作，团队获省级三等奖。`

If output frequency or result is not evidenced, remove it rather than inventing a number.

### Awards

Preserve the official award name, competition level, award grade, and date. Avoid promoting an institution-level award to a provincial or national award.

### Skills

Include only evidenced tools or capabilities. Convert participation evidence into capability wording carefully:

- Evidence: participated in short-video competition
- Safe wording: `具备短视频选题与内容制作实践`
- Unsafe wording without evidence: `精通全平台增长运营`

### Self-evaluation

Use at most two concise bullets. Anchor each trait to evidence when possible. Avoid generic phrases such as `性格开朗、吃苦耐劳、学习能力强` unless space remains and the user requests them.

## Privacy rules

- Keep source files local unless the user authorizes an external service for that specific operation after receiving a disclosure of recipient, fields/files, purpose, and known retention behavior.
- Minimize and, where possible, redact personal fields before any authorized external processing.
- Do not place phone numbers, email addresses, government IDs, or home addresses in logs, skill documentation, or chat summaries.
- Use personal data only inside the requested resume deliverable.
- Do not retain candidate-specific materials in bundled skill resources.
- Store temporary renders inside the approved task workspace, restrict their distribution, and remove them only when the user requests cleanup under the applicable file-safety rules.
- Treat macros, OLE objects, remote templates, external relationships, links, and QR targets as inactive unless separately authorized.
