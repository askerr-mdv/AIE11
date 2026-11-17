# Decisions

One row one decision. This week is the first one. By Week 5 this file will explain what decisions you made during this bootcamp.

## Retrieval, week 1

**What I changed**

> I changed the k, the number of chunks retrieved per question, from 3 to 7. 

**Why**

> Three different variations of questions pertaining to fiber intake yielded different results, including no context results. The related chunk was outside of the k=3. I was curious about that and wanted to make small change now. I was able to correct 2 questions in my test cases, bringing my results from 7/10 to 9/10. The decline questions held up. That’s the regression I was worried about, and it didn’t happen.

**What would change my mind**

> More experiment needed to find a more robust change for such cases since I cannot just adjust the k to account for question variations. Depending on the corpus size and how the app is architected, I might optimize for cost (and save index) instead of edge performance in MVP. Also, the fix only just works (ranks 6 and 7), it costs more context. So would need to see the cost, speed, accuracy tradeoff to make a decision.
> I'd go back to smaller k if cost or speed matters more than those failed questions or if the declined questions started answering from the extra chunks.

