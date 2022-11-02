operations = [
    {"id": 1, "timestamp": 2, "amount": 1},
    {"id": 2, "timestamp": 4, "amount": 8},
    {"id": 1, "timestamp": 3, "amount": 2}
]


def filter(operations: list) -> list:
    result = {}
    for item in operations:
        if not result.get(item['id']):
            result[item['id']] = item
            continue
        if result[item['id']].get('timestamp', 0) < item.get('timestamp', 0):
            result[item['id']] = item
            continue
    return list(result.values())


print(filter(operations))
