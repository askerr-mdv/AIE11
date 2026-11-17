# RAG Test Questions: Personal Wellness Guide

These 10 questions test simple fact retrieval, answers that require evidence from two chunks, and questions the corpus cannot answer.

The expected answers reflect the contents of `HealthWellnessGuide.txt`; they are an evaluation key for the corpus, not independent health advice.

## Chunk settings

- Corpus: `HealthWellnessGuide.txt` — 16,206 characters.
- Chunk size: 1,000 characters.
- Chunk overlap: 200 characters.
- Total: 21 chunks.
- Chunk IDs start at `0`, matching the app's citations.

The evidence locations below were checked against these settings. If you change the corpus or splitting settings, check the chunk IDs again.

## Questions

Send only the question to your app. Keep the answer key separate from the prompt and corpus.

### Category 1: Simple lookup

1. What are the four main types of exercise listed in the guide?
2. How many main dishes does the guide suggest choosing when planning meals for the week?
3. How many minutes does the guide suggest starting with for basic mindfulness meditation?
4. What are the three components of the habit loop, and what does each mean?

### Category 2: Needs two chunks

5. How many days per week should adults do muscle-strengthening activities, and which protein sources does the guide list for muscle repair?
6. What daily targets does the guide give for water in ounces and fiber in grams?
7. What does the guide say about caffeine for headaches, and what caffeine cutoff time does it recommend for better sleep?

### Category 3: Not covered by the corpus

8. What dose of ibuprofen does the guide recommend for treating a migraine?
9. How many milligrams of magnesium does the guide recommend for insomnia, and when should it be taken?
10. What does each “20” in the guide's 20-20-20 rule stand for?

## Answer key

| # | Expected answer or behavior | Supporting evidence |
|---|---|---|
| 1 | Aerobic/cardio, strength training, flexibility, and balance. | Chunk **0**. |
| 2 | **3–4 main dishes**. | Chunk **4 or 5**. |
| 3 | Start with **5 minutes**, then gradually increase. | Chunk **11**. |
| 4 | **Cue:** the trigger; **routine:** the behavior; **reward:** the benefit. | Chunk **12**. |
| 5 | Muscle-strengthening activities on **2 or more days per week**. Protein sources include **lean meats, fish, eggs, legumes, and dairy**. | Chunks **0 and 4**. Both are needed. |
| 6 | A general recommendation of **64 ounces of water**, with individual needs varying, and **25–35 grams of fiber** daily. | Chunk **5 or 6**, plus chunk **14 or 15**. Both evidence groups are needed. |
| 7 | For headaches, caffeine in small amounts **can help or hurt**. For sleep, **avoid caffeine after 2 PM**. | Chunk **14**, plus chunk **7, 8, or 19**. Both evidence groups are needed. |
| 8 | Explicitly acknowledge that the guide does **not** provide an ibuprofen dosage or migraine medication instructions. Do not invent a dose. | No supporting answer exists. Related headache information is in chunk **14**, but it does not provide the requested medication guidance. |
| 9 | Explicitly acknowledge that the guide does **not** specify a magnesium dose or timing. It mentions supplements and consulting a healthcare provider, but gives no regimen. | Related text is in chunks **8 or 9**; neither supplies the requested dose or timing. |
| 10 | Explicitly acknowledge that the guide names the rule but does **not** explain what the numbers mean. An explanation drawn from outside knowledge fails this corpus-grounding test. | The rule is mentioned in chunk **18**, without an explanation. |

## How to score the results

- **Questions 1–4:** The answer must match the guide and cite retrieved evidence that supports it. Equivalent wording is acceptable.
- **Questions 5–7:** The answer must address both parts and cite evidence from both required groups of chunks. A correct answer without supporting retrieved evidence does not demonstrate successful retrieval.
- **Questions 8–10:** The answer must acknowledge the missing information without supplying unsupported details. Related chunks may still be retrieved; the answer must recognize that they do not contain the requested information.

Use `--show-chunks` when running the app so you can inspect what was retrieved. Keep retrieval and answer quality separate when diagnosing a failure:

- **Retrieval failure:** A needed supporting chunk was not retrieved.
- **Answer-generation failure:** The necessary evidence was retrieved, but the answer ignored it, misstated it, or added unsupported claims.
- **Missing-information handling failure:** The answer supplied details the corpus does not contain instead of acknowledging the gap.

For a simple overall score, award one point per question only when the relevant criteria above are satisfied, for a maximum of **10 points**. Record a brief reason for each failure so you can compare the same questions after changing the app.

## Results

### Baseline: `k = 3` (score 7/10)

Raw output: `baseline.txt`

| # | Question | ✅/❌ | What went wrong, where |
|---|----------|------|------------------------|
| 1 | Four main types of exercise? | ✅ | Chunk 0 ranked #1 (0.586). Clean |
| 2 | How many main dishes for weekly meal planning? | ✅ | Chunk 5 ranked #1 (0.482). Clean |
| 3 | Minutes to start mindfulness meditation? | ✅ | Chunk 11 ranked #1 (0.540). Clean |
| 4 | Three components of the habit loop? | ✅ | Chunk 12 ranked #1 (0.554). Clean |
| 5 | Strength-training days and protein sources? | ✅ | Chunks 0 and 4 both retrieved (#2, #3). Unneeded chunk 3 ranked #1 |
| 6 | Daily water (oz) and fiber (g) targets? | ❌ | **Retrieval:** fiber chunk 15 not in top 3 (water chunks 5, 6, 20 filled it). Model correctly said it had no fiber target |
| 7 | Caffeine for headaches, and sleep cutoff time? | ❌ | **Retrieval:** headache chunk 14 not in top 3. Model correctly said it had nothing on headaches |
| 8 | Ibuprofen dose for a migraine? | ✅ | Declined. Top score only 0.241 |
| 9 | Magnesium dose and timing for insomnia? | ✅ | Declined, and cited chunks 8 and 9 for what the guide does say |
| 10 | What each "20" in the 20-20-20 rule means? | ❌ | **Missing-information handling:** guide only names the rule (chunk 18). Model explained it from outside knowledge |

### After: `k = 7` (score 9/10)

Raw output: `after_k.txt`

| # | Baseline | After | What changed |
|---|:---:|:---:|---|
| 1–5 | ✅ | ✅ | Same answers, same top chunks |
| 6 | ❌ | ✅ | Fiber chunk 15 retrieved at **rank 6** (0.329). Answer now gives 64 oz water and 25–35 g fiber |
| 7 | ❌ | ✅ | Headache chunk 14 retrieved at **rank 7** (0.343). Answer now covers both headaches and the 2 PM cutoff |
| 8 | ✅ | ✅ | Still declines. All 7 chunks score ≤ 0.241 |
| 9 | ✅ | ✅ | Still declines, cites chunks 8 and 9 |
| 10 | ❌ | ❌ | **Missing-information handling**, unchanged. Now admits the explanation is "not explicitly detailed" in the context, then gives it anyway |

**Regressions:** none.

**Notes:**

- The fix is at the edge: both needed chunks landed in the last two slots (ranks 6 and 7). A slightly different wording could push them to rank 8 and fail again.
- `k = 7` is a third of the corpus (7 of 21 chunks), so every question now sends about 2.3× more context to the chat model, including simple lookups that only need 1 chunk.
- Raising `k` can't fix Q10, because Q10 is a generation problem, not a retrieval problem. A prompt change would target it.

### Vibe check

> Going from 7/10 to 9/10 is good, but I suspect that raising the k has a limit and can create additional side effects for different Q&A conditions, although it worked in this application.
