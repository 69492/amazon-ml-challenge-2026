# Student Resource Inspection Report

## Scope and method
This report was generated from the local `student_resource/` directory only. No internet, external databases, or external business data were used. The supplied challenge files were read only; this report is the only new artifact created.

## 1. Complete folder/file tree
```text
.DS_Store
dataset/
dataset/.DS_Store
dataset/test/
dataset/test/test_source1.tsv
dataset/test/test_source2.tsv
dataset/test/test_source3.tsv
dataset/train/
dataset/train/train_ground_truth.tsv
dataset/train/train_source1.tsv
dataset/train/train_source2.tsv
dataset/train/train_source3.tsv
Documentation_template.md
README.md
utils/
utils/validate_submission.py
```

## 2-4. File purposes, exact filenames, and sizes

- `.DS_Store` ? 6,148 bytes ? macOS Finder metadata.
- `dataset/.DS_Store` ? 6,148 bytes ? macOS Finder metadata.
- `dataset/test/test_source1.tsv` ? 175,022,086 bytes ? Test source table.
- `dataset/test/test_source2.tsv` ? 509,456,422 bytes ? Test source table.
- `dataset/test/test_source3.tsv` ? 506,002,772 bytes ? Test source table.
- `dataset/train/train_ground_truth.tsv` ? 127,015,583 bytes ? Training source/ground-truth table.
- `dataset/train/train_source1.tsv` ? 210,069,713 bytes ? Training source/ground-truth table.
- `dataset/train/train_source2.tsv` ? 489,301,488 bytes ? Training source/ground-truth table.
- `dataset/train/train_source3.tsv` ? 503,705,637 bytes ? Training source/ground-truth table.
- `Documentation_template.md` ? 2,175 bytes ? Documentation template.
- `README.md` ? 14,130 bytes ? Challenge README/instructions.
- `utils/validate_submission.py` ? 13,687 bytes ? Submission validation utility.

## 17. README.md

```markdown
# ML Challenge 2026 Problem Statement

## Business Entity Resolution Challenge

In large-scale commercial platforms, business identity data arrives from multiple independent sources — each contributing partial, noisy fragments of information about the same real-world entities. These fragments share no common identifiers, and the challenge of determining which records refer to the same business is known as Entity Resolution (ER). Your challenge is to build an ML solution that, given business records from 3 independent data sources with noisy and inconsistent fields, determines which records across sources refer to the same real-world business entity.

Source 1 is the deduplicated reference source. Your task is to find all matching records from Source 2 and Source 3 for each Source 1 entity. A Source 1 entity may match zero, one, or many records from Source 2 and Source 3.

### File Format

**All files in this challenge are tab-separated (`.tsv`), and your submissions must be tab-separated too.** Tabs are used because business addresses and the ID list columns both contain commas. Read them with an explicit tab separator, for example:

```python
import pandas as pd
df = pd.read_csv("dataset/train/train_source1.tsv", sep="\t")
```

Reading a `.tsv` without `sep="\t"` will silently produce a single column containing the whole line.

### Data Description:

Each source file (`*_source1.tsv`, `*_source2.tsv`, `*_source3.tsv`) has the following columns:

1. **entity_id:** Unique identifier for the record. The prefix indicates the source — `S1-`, `S2-`, or `S3-`.
2. **business_name:** Name of the business entity (may contain abbreviations, legal suffixes, typos, transliterations)
3. **business_address:** Address of the business (may contain partial addresses, format variations, missing components, landmark-based references)
4. **country:** Country label for the record. The **training** data covers `US` and `India`. The **test** set additionally contains a third country, `France`, that does **not** appear in the training data. Treat `country` as an open set of string labels: do **not** hard-code, filter, or one-hot your pipeline to only `{US, India}`, and remember that every test entity — `France` included — must appear in your submission.

There is no separate *source* column — a record's source is given by its `entity_id` prefix (`S1-`/`S2-`/`S3-`) and by which file it appears in.

The ground truth file (`train_ground_truth.tsv`) has two columns:

1. **source1_entity_id:** The `entity_id` of a Source 1 record
2. **matched_entity_ids:** Comma-separated list of matching `entity_id`s from Source 2 and/or Source 3 (empty when the entity has no matches)

**Noise Patterns to Expect:**

- **Name variations:** Abbreviations (Corp vs. Corporation, Pvt vs. Private, Ltd vs. Limited), legal suffix inconsistencies, DBA/trade names, punctuation differences (& vs. "and"), word-order transpositions, typos
- **Address variations:** Abbreviations (Rd vs. Road, St vs. Street), transliteration variants, missing components (no PIN code, no state), landmark-based references (Near SBI ATM), municipal numbering formats, component reordering

### Dataset Details:

- **Training Dataset:** Business records across 3 sources with ground truth matching labels
- **Test Set:** Business records across 3 sources without matching labels

### File Descriptions:

*Training files*

1. **dataset/train/train_source1.tsv:** Source 1 training records (the deduplicated reference source)
2. **dataset/train/train_source2.tsv:** Source 2 training records
3. **dataset/train/train_source3.tsv:** Source 3 training records
4. **dataset/train/train_ground_truth.tsv:** Ground truth matching labels for the training set

*Test files*

1. **dataset/test/test_source1.tsv:** Source 1 test records. Generate matches for every entity in this file.
2. **dataset/test/test_source2.tsv:** Source 2 test records
3. **dataset/test/test_source3.tsv:** Source 3 test records

No ground truth is provided for the test set. To measure your own performance, hold out a validation split from the training data and score it yourself using the F_0.5 formula given below.

### Output Format:

Your solution produces **two** tab-separated files, both placed in the `output/`
folder of your final submission package (see *Final Submission Package* below):

1. **`matching_results.tsv`** — your final entity matches. **This is the only file
   scored on the leaderboard** — it is what you upload to the Portal during the challenge.
2. **`candidate_pairs.tsv`** — the candidate set your blocking / candidate-generation
   stage produced, before your final matching model narrowed it down.

#### matching_results.tsv

Your final entity matches:

| Column | Description |
| --- | --- |
| source1_entity_id | The `entity_id` of a Source 1 record |
| matched_entity_ids | Comma-separated list of matching `entity_id`s from Source 2 and/or Source 3 |

**Example** (columns separated by a single tab, ID lists separated by commas with no quoting):

```
source1_entity_id	matched_entity_ids
S1-00001	S2-00047,S2-00193,S3-00812
S1-00002	S3-00004
S1-00003	
```

**Important:**

- Every Source 1 entity in the test set must have exactly one row
- Leave `matched_entity_ids` empty for entities with no matches (singletons)
- No duplicate entity IDs within a single ID list
- ID lists must only contain Source 2 or Source 3 IDs that exist in the test set

#### candidate_pairs.tsv

The candidate set from your blocking stage — every Source 2 / Source 3 record you
considered a plausible match for each Source 1 entity, *before* your final matching
model narrowed it down. This is the **exact set of records you feed into your matching model
for inference** — the final candidate list *just before* the ML model scores them, not
the raw output of an early blocking pass you later filter further. If your pipeline has
several blocking/filtering stages, `candidate_pairs.tsv` is the *last* one: whatever
your model actually runs inference over. Every ID in `matching_results.tsv` should
therefore appear here.

It is **not scored on the leaderboard**; we use it to analyse blocking quality (recall
ceiling, reduction ratio) and to verify your pipeline.

| Column | Description |
| --- | --- |
| source1_entity_id | The `entity_id` of a Source 1 record |
| candidate_entity_ids | Comma-separated list of candidate `entity_id`s from Source 2 and/or Source 3 |

**Example:**

```
source1_entity_id	candidate_entity_ids
S1-00001	S2-00047,S2-00193,S3-00812,S3-00999
S1-00002	S3-00004
S1-00003	
```

Same rules as `matching_results.tsv`: one row per Source 1 entity, `candidate_entity_ids`
empty when blocking found no candidates, S2-/S3- IDs only, no duplicates within a list.
Your final matches should be a **subset** of your candidates (a matched ID that never
appeared as a candidate signals a pipeline bug — the validator warns about it).

**Validate before submitting:** a helper script `utils/validate_submission.py` (stdlib
only, no dependencies) checks both files against every rule above so you can catch a
rejection locally instead of spending a submission on it. Run it from this
`student_resource/` directory:

```bash
python3 utils/validate_submission.py \
    --matching output/matching_results.tsv \
    --candidate output/candidate_pairs.tsv \
    --test-dir dataset/test
```

It prints `PASS` (exit 0) when the files are safe to submit, or a numbered list of issues
to fix (exit 1). It only reads your output files and the test source files; it does not
compute your score.

### Final Submission Package:

In addition to your live leaderboard uploads, **every team submits a single zip
archive** with your code and outputs. We use it to reproduce your results, audit your
blocking, and check the fair-play and model-license rules — the top teams' packages are
reviewed in detail before the final rankings are confirmed.

Structure:

```
<team_name>_submission.zip
├── output/
│   ├── matching_results.tsv        # final matches (same file you upload to the leaderboard)
│   └── candidate_pairs.tsv         # your blocking candidate set
├── code/
│   └── business_entity_resolution/
│       ├── src/                    # all your source code
│       ├── README.md               # how to reproduce end-to-end (data → blocking → matching → output)
│       └── requirements.txt        # pinned dependencies / environment
└── Documentation_template.md       # your methodology write-up (this filled-in template)
```

- **`output/`** — the two TSV files described above: `matching_results.tsv` and
  `candidate_pairs.tsv`.
- **`code/business_entity_resolution/`** — a self-contained, runnable copy of your
  pipeline. Put all source under `src/`, and include a `README.md` with exact run
  instructions plus a `requirements.txt` (or equivalent environment file) pinning
  versions. Anyone should be able to regenerate both output files from the
  training/test data using only what is in this folder.
- **Methodology document** — fill in the provided `Documentation_template.md` and drop
  it straight into the zip (the filled-in `.md` is fine; a `.pdf` export works too). No
  need to rename it.

### Constraints:

1. Format your output exactly as described above. Submissions that fail validation will not be evaluated. You should see a `SCORED` status with your F_0.5 score if the output is correctly formatted.
2. `matched_entity_ids` must only reference entities from Source 2 or Source 3. Self-matches to Source 1, and IDs that do not exist in the test set, will be rejected.
3. Every Source 1 entity must appear in your submission. Missing entities will cause rejection.
4. Duplicate entity IDs in any ID list will cause rejection, as will duplicate `source1_entity_id` rows.
5. Final model should be a MIT/Apache 2.0 License model and up to 8 Billion parameters.

### Evaluation Criteria:

Submissions are evaluated using **F_β Score (β = 0.5)** — a precision-heavy metric that penalizes false merges (matching two different businesses) more than missed matches.

**Formula:**

```
F_0.5 = (1.25 × Precision × Recall) / (0.25 × Precision + Recall)
```

Computed as a **macro-average**: F_0.5 is calculated per Source 1 entity, then averaged across **all** Source 1 entities in the evaluation set.

Singletons are included in that average. A Source 1 entity with no true matches scores 1.0 when you correctly predict an empty list, and 0.0 when you predict any match for it. Correctly identifying singletons therefore earns credit, and false merges on them are penalised.

**Why precision-heavy?** In real-world entity resolution, merging two distinct businesses (false positive) is more damaging than missing a link (false negative). F_0.5 weights precision 2× over recall.

**Example:**

- Your model predicts S1-00001 matches [S2-00047, S2-00193, S3-00812]
- Ground truth says S1-00001 matches [S2-00047, S3-00812]
- Precision = 2/3, Recall = 2/2 = 1.0
- F_0.5 = (1.25 × 0.667 × 1.0) / (0.25 × 0.667 + 1.0) = **0.714**

### Leaderboard Information:

- **Public Leaderboard:** During the challenge, rankings will be based on a subset of the test set to provide real-time feedback on your model's performance.
- **Private Leaderboard:** After the challenge ends, the private leaderboard will be revealed, which uses the remaining portion of the test set for evaluation.
- **Final Rankings:** The final decision will be based on the private leaderboard.

You submit predictions for the full test set in both cases; the split is applied during scoring.

### Submission Requirements:

1. **Leaderboard (during the challenge):** upload `matching_results.tsv` in the Portal —
   tab-separated, with the exact column names described above. This is what drives the
   public and private leaderboards.
2. **Final submission package:** submit the single zip described in *Final Submission
   Package* above — `output/` with **both** `matching_results.tsv` (final matches) and
   `candidate_pairs.tsv` (your candidate-generation / blocking set fed to the model),
   `code/business_entity_resolution/` (runnable pipeline), and your methodology document.
   All teams must submit it; the top teams' packages are reviewed before the final
   rankings are confirmed.
3. Your methodology document must describe:
   - Methodology used
   - Candidate generation / blocking strategy
   - Model architecture and feature engineering
   - Any other relevant information about the approach

   A template for this documentation is provided in `Documentation_template.md`. There is no page limit — prioritise clarity and technical depth over brevity.

### **Academic Integrity and Fair Play:**

**⚠️ STRICTLY PROHIBITED: External Data Lookup**

Participants are **STRICTLY NOT ALLOWED** to use external databases, APIs, or services to look up business identities or resolve entities. This includes but is not limited to:

- Using commercial entity resolution APIs or services
- Looking up business registrations from government databases
- Using geocoding APIs to normalize addresses
- Any external data augmentation from internet sources

**Enforcement:**

- All submitted approaches, methodologies, and code pipelines will be thoroughly reviewed and verified
- Any evidence of external data lookup will result in **immediate disqualification**

**Fair Play:** This challenge is designed to test your machine learning and data science skills using only the provided training data.

### Tips for Success:

- Invest in a strong blocking/candidate generation strategy — it determines the upper bound of your recall
- Explore string similarity features (Jaccard, Levenshtein, TF-IDF cosine) for name and address matching
- Pay attention to country specific address patterns
- Consider the precision-recall trade-off carefully — F_0.5 rewards precision more than recall
- Do not neglect singletons — correctly predicting "no match" is worth a full 1.0 on that entity
- Validate your own output format against the rules above before submitting
```

## 17. Documentation_template.md

```markdown
# ML Challenge 2026: Business Entity Resolution Solution Template

**Team Name:** [Your Team Name]  
**Team Members:** [List all team members]  
**Submission Date:** [Date]

---

## 1. Executive Summary
*Provide a brief 2-3 sentence overview of your approach and key innovations.*

---

## 2. Methodology

### 2.1 Problem Analysis
*Key insights discovered during EDA — noise patterns, address variations, missing fields, etc.*

### 2.2 Solution Strategy
*Outline your high-level approach.*

**Approach Type:** [Blocking + Classifier / End-to-End / Graph-Based / Hybrid, etc]  
**Core Innovation:** [Brief description of your main technical contribution]

---

## 3. Candidate Generation (Blocking)
*Describe how you reduced the comparison space to a manageable candidate set.*

- **Blocking keys used:** [e.g., PIN code, phonetic name encoding, TF-IDF, etc.]
- **Candidate pairs generated:** [total]
- **How you ensured true matches were not lost:**

---

## 4. Matching Model

**Features used:**
- Name features: [e.g., Jaccard, Levenshtein, phonetic encoding]
- Address features: [e.g., token overlap, edit distance, PIN code matching]
- Other: []

**Model type:** [e.g., XGBoost, Siamese Network, Transformer, etc.]  
**Threshold selection method:** [e.g., F_0.5 optimization on validation set]

---

## 5. Results & Error Analysis

- **F_0.5 Score (macro):** [your best validation score]
- **Common false positives (wrong merges):** [brief description]
- **Common false negatives (missed matches):** [brief description]

---

## 6. Conclusion
*Summarize your approach, key achievements, and lessons learned in 2-3 sentences.*

---

## Appendix

### A. Code Artefacts
*Your complete, runnable code ships in the submission zip under
`code/business_entity_resolution/` (all source in `src/`, with a `README.md` and
`requirements.txt`). Summarise its structure and the entry point(s) to reproduce
`output/matching_results.tsv` and `output/candidate_pairs.tsv` here.*

### B. Additional Results
*Include any additional charts, graphs, or detailed results.*

---

**Note:** Teams can modify sections according to their approach while maintaining clarity and technical depth.
```

## 5-11. Dataset profiling

### `dataset/test/test_source1.tsv`

- File size: **175,022,086 bytes**
- Shape: **1,732,544 rows x 4 columns**
- Columns: `entity_id`, `business_name`, `business_address`, `country`
- Data types: all fields were parsed as text to preserve IDs and leading zeros; empty fields are missing.
- Missing values: `entity_id`=0; `business_name`=0; `business_address`=0; `country`=0
- Unique values: `entity_id`=1,732,544; `business_name`=1,238,867; `business_address`=1,677,483; `country`=3
- Duplicate rows: **0**
- First 5 rows:
```text
S1-714132312	Zephay Labs Inc	2621 Cotten Road, Tyler, TX	US
S1-106407869	Vision Partners Corp	IA, Iowa City, 1064 Newton Rd, Unit 11	US
S1-156285671	<< Team Ecole	175 Boulevard du Président Franklin Roosevelt, Bordeaux, Nouvelle-Aquitaine	France
S1-689823050	Red Perfect Trading	Mirzapur, Ews 12, Uttar Pradesh, Mirzapursadar, Awas Vikas Colony	India
S1-921369899	ZNB Club SARL	Nouvelle-Aquitaine, La Teste-de-Buch, 5 bis Rue Pierre Dignac	France
```

### `dataset/test/test_source2.tsv`

- File size: **509,456,422 bytes**
- Shape: **4,887,273 rows x 4 columns**
- Columns: `entity_id`, `business_name`, `business_address`, `country`
- Data types: all fields were parsed as text to preserve IDs and leading zeros; empty fields are missing.
- Missing values: `entity_id`=0; `business_name`=0; `business_address`=129,408; `country`=0
- Unique values: `entity_id`=4,887,273; `business_name`=4,311,041; `business_address`=4,224,784; `country`=3
- Duplicate rows: **0**
- First 5 rows:
```text
S2-192345572	Brahma Infosoft	COIMATORE COLONY, HUNSUR TQMYSORE DIST., Karnataka	India
S2-566025912	Marina Ecole France Sarl	63 R. DE DIEPPE, LILLE, Hauts-de-France	France
S2-158121477	SCI Ptit Àmicale	18 RUE JEN ZAY, Dunkerque, Nord	France
S2-89663826	Apex Summit	67 KENTUCKY ST, SALYERSVILLE, KY	US
S2-884102769	Fresh Truist	8264 FILLY COURT, ROANOKE COUNTY, VA	US
```

### `dataset/test/test_source3.tsv`

- File size: **506,002,772 bytes**
- Shape: **5,082,316 rows x 4 columns**
- Columns: `entity_id`, `business_name`, `business_address`, `country`
- Data types: all fields were parsed as text to preserve IDs and leading zeros; empty fields are missing.
- Missing values: `entity_id`=0; `business_name`=0; `business_address`=136,098; `country`=0
- Unique values: `entity_id`=5,082,316; `business_name`=4,521,929; `business_address`=4,456,436; `country`=3
- Duplicate rows: **0**
- First 5 rows:
```text
S3-462677478	मॉडर्न फाइनेंस	No 10 Enkay Square, 448A, Udyog Vihar Phase V, Gurugram, Gurgaon, HR	India
S3-374810425	Shri Sai Infratech Co	3/115, East Delhi, DL	India
S3-198586129	Fractales Amis Groupe S.A.S	23 Rue Icmre, La Teste-de-buch, Gironde	France
S3-10300249	Shri Supreme Consulting Private  (Limited)	H.no 910 A 3503, Mumbai, महाराष्ट्र	India
S3-604980231	Prime Realty Ventures Public Limited	G.t. Karnal Road, Industrial Area, New Delhi, null, A-68, दिल्ली	India
```

### `dataset/train/train_ground_truth.tsv`

- File size: **127,015,583 bytes**
- Shape: **2,206,821 rows x 2 columns**
- Columns: `source1_entity_id`, `matched_entity_ids`
- Data types: all fields were parsed as text to preserve IDs and leading zeros; empty fields are missing.
- Missing values: `source1_entity_id`=0; `matched_entity_ids`=123,247
- Unique values: `source1_entity_id`=2,206,821; `matched_entity_ids`=2,083,575
- Duplicate rows: **0**
- First 5 rows:
```text
S1-965667	S2-681193310,S2-743505751,S3-775321672,S3-11291185,S3-860443364
S1-55344266	S2-249013014,S2-197070651,S3-478195123,S3-384364074
S1-343815751	S2-790675320,S2-479876582,S3-878454467
S1-656753428	S2-153058913,S2-24659151,S3-679606215
S1-102811957	S2-478959098,S2-553508714,S2-625774905,S3-728090388,S3-928796641,S3-449308785
```

### `dataset/train/train_source1.tsv`

- File size: **210,069,713 bytes**
- Shape: **2,206,821 rows x 4 columns**
- Columns: `entity_id`, `business_name`, `business_address`, `country`
- Data types: all fields were parsed as text to preserve IDs and leading zeros; empty fields are missing.
- Missing values: `entity_id`=0; `business_name`=0; `business_address`=0; `country`=0
- Unique values: `entity_id`=2,206,821; `business_name`=1,539,229; `business_address`=2,130,606; `country`=2
- Duplicate rows: **0**
- First 5 rows:
```text
S1-925783039	Orelee's Barbershop	1795 Westchester Drive, High Point, NC	US
S1-773889195	Prime Money	17560 Ellis Road, Tahlequah, OK	US
S1-377745466	B+ Retail Inc	1712 Montebello Avenue, Phoenix, AZ	US
S1-133037285	Christ Chapel	2100 Cameron Drive, Unit APARTMENT G, Dundalk, MD	US
S1-755362802	Prabhav Business Center	797, Lake Town Block A, Kolkata, Howrah, West Bengal	India
```

### `dataset/train/train_source2.tsv`

- File size: **489,301,488 bytes**
- Shape: **5,034,616 rows x 4 columns**
- Columns: `entity_id`, `business_name`, `business_address`, `country`
- Data types: all fields were parsed as text to preserve IDs and leading zeros; empty fields are missing.
- Missing values: `entity_id`=0; `business_name`=0; `business_address`=168,967; `country`=0
- Unique values: `entity_id`=5,034,616; `business_name`=4,402,009; `business_address`=4,337,262; `country`=2
- Duplicate rows: **0**
- First 5 rows:
```text
S2-166376419	राम मार्केटिंग प्राइवेट लिमिटेड	KH NO. -570/13, NEW DELHI, WEST DELHI, Delhi	India
S2-764573417	-- Holloway Peak Inc Seafood	105 ELM ST, MORGANTON, NC	US
S2-639257739	आदित्य प्रॉपर्टीज एलएलपी	G-3/571, GULMOHAR COLONY, BHOPAL, Madhya Pradesh	India
S2-163963287	Summit Inc	GREENSBORO, NC, 19 1/2 STARDUST TRAIL	US
S2-49942811	Delta Tetlecommunication Inc	914 PIERPONT AVE, CLEVELAND, OH	US
```

### `dataset/train/train_source3.tsv`

- File size: **503,705,637 bytes**
- Shape: **5,285,603 rows x 4 columns**
- Columns: `entity_id`, `business_name`, `business_address`, `country`
- Data types: all fields were parsed as text to preserve IDs and leading zeros; empty fields are missing.
- Missing values: `entity_id`=0; `business_name`=0; `business_address`=175,916; `country`=0
- Unique values: `entity_id`=5,285,603; `business_name`=4,651,609; `business_address`=4,632,765; `country`=2
- Duplicate rows: **0**
- First 5 rows:
```text
S3-202863386	wilfordhancock.com	Mack Rd, Haltom City, Texas	US
S3-859268022	International South Consultants Private Ltd		India
S3-22467283	LLC Moncada Léarning Center	5780 Fawn Ct, Fort Worth, Texas	US
S3-671162755	Moyna's Coffee	1 Ivanhoe Ave, PO Box 6009, Cincinnati, Ohio	US
S3-960981775	Pvt. EFS Print Ventures Ltd.	Door No 183, 41St Cross, 22Nd Main 9Th Block Jayanagar, Bengaluru Urban, Bangalore, ಕರ್ನಾಟಕ	India
```

## 12. Country/value distributions

### `dataset/test/test_source1.tsv`
- `country`: US=663,106; France=259,452; India=809,986

### `dataset/test/test_source2.tsv`
- `country`: India=2,312,565; France=703,378; US=1,871,330

### `dataset/test/test_source3.tsv`
- `country`: India=2,405,000; France=731,615; US=1,945,701

### `dataset/train/train_ground_truth.tsv`

### `dataset/train/train_source1.tsv`
- `country`: US=1,323,633; India=883,188

### `dataset/train/train_source2.tsv`
- `country`: India=2,017,799; US=3,016,817

### `dataset/train/train_source3.tsv`
- `country`: US=3,170,056; India=2,115,547

## 13-15. Train, ground-truth, and test structure

Training source tables: `dataset/train/train_source1.tsv`, `train_source2.tsv`, and `train_source3.tsv`; ground truth: `dataset/train/train_ground_truth.tsv`; test source tables: `dataset/test/test_source1.tsv`, `test_source2.tsv`, and `test_source3.tsv`. Detailed shapes and schemas are listed above.

## 18. Likely semantic column mapping

- `dataset/test/test_source1.tsv` columns: `entity_id`, `business_name`, `business_address`, `country`
- `dataset/test/test_source2.tsv` columns: `entity_id`, `business_name`, `business_address`, `country`
- `dataset/test/test_source3.tsv` columns: `entity_id`, `business_name`, `business_address`, `country`
- `dataset/train/train_ground_truth.tsv` columns: `source1_entity_id`, `matched_entity_ids`
- `dataset/train/train_source1.tsv` columns: `entity_id`, `business_name`, `business_address`, `country`
- `dataset/train/train_source2.tsv` columns: `entity_id`, `business_name`, `business_address`, `country`
- `dataset/train/train_source3.tsv` columns: `entity_id`, `business_name`, `business_address`, `country`

The source-specific ID, business-name, address, country, and ground-truth roles are identified from the supplied field names in the schema above. Ground-truth linkage fields are in `train_ground_truth.tsv`; source entity IDs are the `id` fields in the corresponding source files.

## 19. Matches per Source 1 entity

- Ground truth has one row per Source 1 entity, with matches stored as a comma-separated list in `matched_entity_ids`.
- Source 1 entities / ground-truth rows: **2,206,821**.
- Distribution: **0 matches**=123,247; **1 match**=119,157; **2 matches**=375,212; **3+ matches**=1,589,205.

## 20. Train/test country and distribution comparison

Country/value distributions are reported above for every low-cardinality field, including country-like fields. Train and test contain the same three source families; exact country counts can be compared directly in the per-file distributions above.

## 16. Utility/validator scripts

`utils/validate_submission.py` is provided. Source:
```python
#!/usr/bin/env python3
"""
ML Challenge 2026 — Submission Validator

Run this BEFORE submitting. It checks your output files against every formatting
rule the scorer enforces, so you can catch a rejection locally instead of burning
a submission. It reads only your output files and the test source files (to learn
which S1 entities are required and which S2/S3 IDs exist); it never needs the
ground truth and never computes your score.

It validates two files:

* ``matching_results.tsv`` (required) — your final matches, the file scored on the
  leaderboard.
* ``candidate_pairs.tsv`` (optional) — the candidate set from your blocking stage.
  When present, the validator also checks that your final matches are a subset of
  your candidates and *warns* (never fails) otherwise. When absent it is skipped
  with a warning; it is still expected in your final submission zip.

Stdlib only, Python 3.8+. Run from the ``student_resource/`` directory::

    python3 utils/validate_submission.py \
        --matching output/matching_results.tsv \
        --candidate output/candidate_pairs.tsv \
        --test-dir dataset/test

Exit code 0 means the files are safe to submit; 1 means fix the listed issues
(warnings never fail the run).

ID-existence check (off by default). By default the validator does NOT check that
every matched/candidate ID actually exists in the test set: that check loads all
Source-2/3 IDs into memory, which on the full ~1.7M-entity test set costs a few GB
(more when ``candidate_pairs.tsv`` is included). The default run therefore stays fast
and light and verifies every other rule; it prints a warning noting the check was
skipped. Pass ``--check-ids`` to turn it on (it reads ``test_source2.tsv`` /
``test_source3.tsv`` from ``--test-dir``); a missing/garbage matched ID only lowers
your score rather than being rejected by the scorer, so this check is a diagnostic,
not a gate. If ``--check-ids`` runs out of memory, drop ``--candidate`` (the candidate
cross-check is the biggest memory user, and the matching file is the only one scored).
"""

import argparse
import os
import sys

DELIM = "\t"
MAX_EXAMPLES = 5  # how many offending IDs to show per issue
MATCHING_HEADER = ["source1_entity_id", "matched_entity_ids"]
CANDIDATE_HEADER = ["source1_entity_id", "candidate_entity_ids"]


def read_ids(path):
    """Return the set of first-column entity IDs from a source TSV.

    The header row is skipped and blank lines are ignored.
    """
    with open(path, encoding="utf-8") as f:
        next(f, None)  # skip header
        return {line.split(DELIM, 1)[0].strip() for line in f if line.strip()}


def examples(items):
    """Return a short, human-readable sample of ``items`` for an error message."""
    items = sorted(items)
    shown = ", ".join(items[:MAX_EXAMPLES])
    if len(items) > MAX_EXAMPLES:
        return f"{len(items)} total, e.g. {shown}, ..."
    return shown


def load_match_targets(test_dir, warnings):
    """Return the set of valid S2/S3 match IDs, or ``None`` if unavailable.

    Only called when ``--check-ids`` is on. When ``test_source2.tsv`` or
    ``test_source3.tsv`` is missing we cannot check that matched IDs exist, so we
    record a warning and return ``None`` to signal that the existence check should be
    skipped.
    """
    targets = set()
    for name in ("test_source2.tsv", "test_source3.tsv"):
        path = os.path.join(test_dir, name)
        if not os.path.isfile(path):
            warnings.append(
                f"{path} not found — skipping the (optional) check that matched "
                f"IDs exist in the test set. Every other rule is still checked. "
                f"This is the lighter-memory mode; provide test_source2/3.tsv to "
                f"enable the ID-existence check."
            )
            return None
        targets |= read_ids(path)
    return targets


def validate_id_list_file(path, expected_header, col_label, required, valid_ids, errors):
    """Validate one results-style TSV (matching or candidate).

    Applies the shared formatting rules and appends any problems to ``errors``.
    Returns a ``{source1_id: set(matched/candidate ids)}`` mapping, or ``None`` on a
    fatal problem (missing file, empty file, or a broken header) that stops parsing.
    """
    if not os.path.isfile(path):
        errors.append(f"File not found: {path}")
        return None

    name = os.path.basename(path)
    mapping = {}
    seen, dup_rows, intra_dupes = set(), set(), set()
    self_matches, wrong_prefix, unknown = set(), set(), set()
    n_rows = empties = 0

    with open(path, encoding="utf-8") as f:
        header = f.readline()
        if not header:
            errors.append(f"{name} is empty.")
            return None
        if DELIM not in header and "," in header:  # the #1 mistake: a CSV
            errors.append(
                f"{name}: header has no TAB but contains commas — the file looks "
                "COMMA-separated. Submissions must be TAB-separated (.tsv); "
                "write it with df.to_csv(sep='\\t', index=False)."
            )
            return None
        cols = [c.strip().lower() for c in header.rstrip("\n").split(DELIM)]
        if cols != expected_header:
            errors.append(
                f"{name}: unexpected header {cols}. "
                f"Expected exactly {expected_header} (tab-separated)."
            )
            return None

        for line_num, line in enumerate(f, start=2):
            s1, tab, rest = line.partition(DELIM)
            if not tab:
                if s1.strip():
                    errors.append(
                        f"{name}: malformed row (no tab) at line {line_num}: "
                        f"{line.rstrip()!r}"
                    )
                continue

            n_rows += 1
            if s1 in seen:
                dup_rows.add(s1)
            seen.add(s1)

            ids = rest.rstrip("\n").split(",") if rest.strip() else []
            if not ids:
                empties += 1
                mapping[s1] = set()
                continue
            if len(ids) != len(set(ids)):
                intra_dupes.add(s1)
            id_set = set(ids)
            mapping[s1] = id_set
            for mid in id_set:
                if mid.startswith("S1-"):
                    self_matches.add(mid)
                elif not mid.startswith(("S2-", "S3-")):
                    wrong_prefix.add(mid)
                elif valid_ids is not None and mid not in valid_ids:
                    unknown.add(mid)

    # Aggregate the per-category findings. Each entry is (offenders, message);
    # only non-empty categories become errors.
    findings = [
        (
            dup_rows,
            "{name}: duplicate source1_entity_id row(s): {ex}. "
            "Each S1 entity may appear on only one row.",
        ),
        (
            intra_dupes,
            "{name}: repeated ID inside a {col} list for: {ex}. "
            "No duplicate IDs are allowed within a list.",
        ),
        (
            self_matches,
            "{name}: {col} contains Source-1 IDs (self-matches): {ex}. "
            "Only S2-/S3- IDs are allowed.",
        ),
        (
            wrong_prefix,
            "{name}: {col} contains IDs without an S2-/S3- prefix: {ex}.",
        ),
        (
            unknown,
            "{name}: {col} references IDs not in the test "
            "Source-2/3 files: {ex}.",
        ),
        (
            required - seen,
            "{name}: required S1 entity(ies) missing: {ex}. "
            "Every entity in test_source1.tsv needs a row (empty = no match).",
        ),
        (
            seen - required,
            "{name}: row(s) using an S1 ID that is not in the test set: {ex}.",
        ),
    ]
    for offenders, message in findings:
        if offenders:
            errors.append(message.format(name=name, ex=examples(offenders), col=col_label))

    print(f"  {name}: {n_rows} rows ({empties} empty, {n_rows - empties} non-empty).")
    return mapping


def validate(matching_path, candidate_path, test_dir, check_ids=False):
    """Validate the submission output(s); return ``(errors, warnings)`` lists.

    ``check_ids`` (``--check-ids``) turns on the optional, memory-heavy check that
    every matched/candidate ID exists in the test Source-2/3 files. It is off by
    default so the common run stays fast and light.
    """
    errors, warnings = [], []

    source1 = os.path.join(test_dir, "test_source1.tsv")
    if not os.path.isfile(source1):
        errors.append(f"Test source1 file not found: {source1} (check --test-dir).")
        return errors, warnings
    required = read_ids(source1)
    print(f"  required S1 entities: {len(required)}")

    if check_ids:
        valid_ids = load_match_targets(test_dir, warnings)
        if valid_ids is not None:
            print(f"  valid S2/S3 match IDs: {len(valid_ids)}")
    else:
        valid_ids = None
        warnings.append(
            "ID-existence check is OFF (the default) — not checking that matched/"
            "candidate IDs exist in the test set. Every other rule is still checked. "
            "Re-run with --check-ids to enable it (needs test_source2/3.tsv; uses "
            "more memory). A nonexistent ID only lowers your score, never rejects "
            "your submission."
        )

    matched = validate_id_list_file(
        matching_path, MATCHING_HEADER, "matched_entity_ids", required, valid_ids, errors
    )

    # candidate_pairs.tsv is optional: if it's absent we skip its checks with a
    # warning (it's still expected in your final submission zip). A missing
    # candidate file never fails this run on its own.
    candidate = None
    if candidate_path and os.path.isfile(candidate_path):
        candidate = validate_id_list_file(
            candidate_path, CANDIDATE_HEADER, "candidate_entity_ids",
            required, valid_ids, errors,
        )
    elif candidate_path:
        warnings.append(
            f"{candidate_path} not found — skipping candidate_pairs.tsv checks. "
            "It is optional here, but your final submission zip must include "
            "output/candidate_pairs.tsv."
        )

    # Soft check: your final matches should come from your blocking candidates.
    # A matched ID absent from candidate_pairs.tsv usually means a pipeline bug,
    # so we warn but never fail on it.
    if matched is not None and candidate is not None:
        offenders = {
            s1 for s1, mids in matched.items() if mids - candidate.get(s1, set())
        }
        if offenders:
            warnings.append(
                f"{len(offenders)} S1 entity(ies) have matched IDs not present in "
                f"candidate_pairs.tsv, e.g. {examples(offenders)}. Final matches "
                "normally come from your blocking candidates — double-check these."
            )

    return errors, warnings


def main():
    parser = argparse.ArgumentParser(
        description="Validate ML Challenge 2026 submission output files before submitting."
    )
    parser.add_argument(
        "--matching",
        "-m",
        default="output/matching_results.tsv",
        help="Path to matching_results.tsv (default: %(default)s)",
    )
    parser.add_argument(
        "--candidate",
        "-c",
        default=None,
        help="Path to candidate_pairs.tsv "
        "(default: output/candidate_pairs.tsv if it exists).",
    )
    parser.add_argument(
        "--test-dir",
        "-t",
        default="dataset/test",
        help="Folder with test_source1/2/3.tsv (default: %(default)s). "
        "test_source2/3.tsv are only read when --check-ids is given.",
    )
    parser.add_argument(
        "--check-ids",
        action="store_true",
        help="Also check that every matched/candidate ID exists in the test "
        "Source-2/3 files. Off by default (loads all S2/S3 IDs into memory — a few "
        "GB on the full test set). A nonexistent ID only lowers your score, so this "
        "is a diagnostic, not a submission gate.",
    )
    args = parser.parse_args()

    # candidate_pairs.tsv is optional; default to the conventional path and let
    # validate() skip (with a warning) if the file isn't there.
    candidate_path = args.candidate or "output/candidate_pairs.tsv"

    print("ML Challenge 2026 — submission validator")
    print(f"  test dir: {args.test_dir}")
    try:
        errors, warnings = validate(
            args.matching, candidate_path, args.test_dir, check_ids=args.check_ids
        )
    except UnicodeDecodeError:
        print()
        print("FAIL — 1 issue(s) to fix before submitting:")
        print(
            f"  1. A file is not valid UTF-8 text (most likely {args.matching} or "
            f"{candidate_path}). Re-save it as a plain UTF-8, tab-separated .tsv — "
            "not cp1252/Latin-1, and not a compressed or binary file (.gz/.xlsx/"
            ".parquet) renamed to .tsv. In pandas: "
            "df.to_csv(path, sep='\\t', index=False, encoding='utf-8')."
        )
        return 1
    except OSError as exc:
        print()
        print("FAIL — 1 issue(s) to fix before submitting:")
        print(f"  1. Could not read a file: {exc}.")
        return 1

    print()
    for warning in warnings:
        print(f"WARNING: {warning}")
    if errors:
        print(f"FAIL — {len(errors)} issue(s) to fix before submitting:")
        for i, error in enumerate(errors, 1):
            print(f"  {i}. {error}")
        return 1w
    print("PASS — no blocking issues found. Safe to submit.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

## Important limitations

- Streaming analysis treats empty strings as missing and reads every TSV field as text.
- Duplicate rows are counted using a row hash set; this avoids loading full tables into pandas.
- Semantic role mapping is based on provided names and table context only; no external validation was performed.
- Empty directories are not listed as files.
