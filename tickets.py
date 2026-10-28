import json
with open('data.json') as f:
    data = json.load(f)

    a = 0
    for dt in data:
        if dt['priority'] == 'high' and dt['status'] == 'open':
            a = a+1
            print(f'#{dt['id']} {dt['title']}')
    label = 'ticket' if a == 1 else  "tickets"
    print(f'There is {a} urgent {label}')

