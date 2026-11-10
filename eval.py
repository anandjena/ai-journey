import time
from reg import answer_question

TESTS = [
    ("How long does express shipping take?", ["2 business days"]),
    ("What does express delivery cost?", ["150"]),
    ("Can I return an item after 45 days?", ["30 days", "30-day"]),
    ("How long do refunds take after inspection?", ["7 business days"]),
    ("How soon must I report a damaged product?", ["48 hours"]),
    ("Is accidental damage covered by the warranty?", ["not", "does not", "doesn't"]),
    ("Can I cancel my order after it has shipped?", ["may not", "not be possible", "return"]),
    ("Do you ship internationally?", ["don't know", "do not know"]),
    ("Do you offer gift cards?", ["don't know", "couldn't find"]),
    ("What is the capital of France?", ["don't know", "couldn't find"]),
]

passed_count = 0
errors = 0
for question,expected in TESTS:
    answer,matches = answer_question(question)

    if answer is None:
        errors += 1
        print(f"Question: {question}\nResult: ERROR (API problem, not counted)\n")
        time.sleep(13)
        continue
    text = answer.lower().replace("’", "'")
    passed = any(e in text for e in expected)
    if passed:
        passed_count +=1
        print(f"Question :- {question}.\n\nAnswer :- {answer}\n\nResult:- PASS")
    else:
        print(f"Question :- {question}.\n\nAnswer :- {answer}\n\nResult:- FAIL")
    time.sleep(13)

print(f'Total accuracy :- {passed_count}/{len(TESTS)}')
print(f"Passed = {passed_count}, failed = {len(TESTS) - passed_count - errors}, errors = {errors}")