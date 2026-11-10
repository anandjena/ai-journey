from reg import retrive

question = input("Ask anything: ")

matches = retrive(question,'knowledge',4)

if not matches:
    raise SystemExit("I can not find anything relevant")

print(matches[0][1])
