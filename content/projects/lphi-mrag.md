---
title: "LPHI-mRAG"
full_title: "Language preference and hallucination in multilingual retrieval-augmented generation"
summary: "Do language models prefer some languages over others when answering from documents? We test this for chatbots that answer questions from a collection of documents in several languages."
project_type: research    # research | applied
funder: ""                # TODO: funder
start: 2026
end: "2026-08"            # empty while running; then a year (2026) or year-month ("2026-10")
themes: ["languages", "llm-trust"]
people: ["sandra-mitrovic", "david-kletz", "fabio-rinaldi"] # TODO: add the people working on it (folder names in content/people)
partners: []
links: []
---
Chatbots that answer questions from your own documents (retrieval-augmented
generation) first search for relevant texts and then let a language model write an
answer from them. What the search returns strongly shapes the answer, and language
models sometimes make things up (hallucinate).

The effect of how many documents are given, and in which order, has been studied. The
effect of their language has not. In a multilingual country like Switzerland, the
useful document is often in a different language from the question. We study whether
language models, although presented as multilingual, prefer some languages, and
whether this leads to more hallucinations.
