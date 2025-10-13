from JsonDecorator import load_from_json

results = load_from_json("results.json")
parties = load_from_json("parties.json")

votes_total = sum([i for i in results.values()])

results_by_percentage = []

for party_name in results.keys():
    votes = results[party_name]
    party_name = parties[party_name]["name"]

    try:
        percentage = votes / votes_total * 100
        results_by_percentage.append([party_name, percentage])
    except ZeroDivisionError:
        results_by_percentage.append([party_name, 0])

results_by_percentage.sort(key=lambda x: x[1], reverse=True)

for result in results_by_percentage:
    print(f"{result[0]}: {result[1]}%")
