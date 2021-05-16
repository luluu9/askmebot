import json
data = {
    "questions": {
    },
    "topics": {
    }
}

questions = []
with open("questions.txt", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        questions.append(line.strip())

for ind, question in enumerate(questions, start=1):
    data['questions'][ind] = question

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

