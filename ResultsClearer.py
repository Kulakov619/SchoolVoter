from JsonDecorator import load_from_json, save_to_json

results = {}
parties = load_from_json("parties.json")

for i in range(1, len(parties) + 1):
    results[str(i)] = 0

save_to_json(results, "results.json")
