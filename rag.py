from reg import retrive,ask_llm,build_prompt,answer_question

question = input("Ask something: ")

answer, matches = answer_question(question)

print("\nAnswer: ",answer)
print("\n Sources:")

for score, doc in matches:
    print(f" {score:.3f} {doc}")








