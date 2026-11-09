import collections, requests
B = "http://127.0.0.1:9000"

r = requests.post(f"{B}/predict", json={"features": [[5.1, 3.5, 1.4, 0.2]]})
assert r.status_code == 200 and len(r.json()["prediction"]) == 1, r.text
print("predict OK:", r.json())

r = requests.post(f"{B}/update-model", json={"version": "1"})
assert r.status_code == 200 and r.json()["next_version"] == "1", r.text
assert requests.get(f"{B}/status").json()["next_version"] == "1"
print("update-model OK")

c = collections.Counter(
    requests.post(f"{B}/predict", json={"features": [[6.0, 3.0, 4.8, 1.8]]}).json()["used"]
    for _ in range(200))
print("repartition canary:", dict(c))

r = requests.post(f"{B}/accept-next-model")
assert r.status_code == 200
print("accept-next-model OK:", r.json())
