---
title: "BM-TOK"
full_title: "Balancing multilingual token vocabularies"
summary: "How to build the vocabulary of a multilingual language model so that less-resourced languages and non-Latin scripts are represented fairly."
project_type: research    # research | applied
funder: ""                # TODO: funder
start: 2026
end: "2027-01"            # empty while running; then a year (2026) or year-month ("2026-10")
themes: ["languages"]
people: ["vani-kanjirangat", "david-kletz", "tanja-samardzic", "fabio-rinaldi"]
partners: []
links: []
---
Language models are becoming multilingual, but languages are not covered equally.
Even in Apertus, the Swiss open language model, where 40% of the training data is
not English, most data comes from a few large languages. Less-resourced languages get
lower-quality output, and non-Latin scripts are often poorly represented in the
model's vocabulary, which also makes these languages more expensive to process.

A key factor is tokenization: how text is split into the pieces (tokens) that make up
the model's vocabulary. Once a model is trained, an unbalanced vocabulary is hard to
fix. We ask how vocabularies can be designed from the start to represent
less-resourced languages fairly.

We test whether making texts in different languages come out at a similar number of
tokens is a good goal for building the vocabulary. To measure the effect, we train
smaller models from scratch while varying the tokenization in a controlled way.
