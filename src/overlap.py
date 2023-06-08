import json
import math
import sys
from client import SearchClient
import functools

class OverlapClient:

    def __init__(self, engines) -> None:
        assert len(engines) == 2, "expect comparing only two engines"
        print(f"engines: left: `{engines[0]}`, right: `{engines[1]}`")
        self.left = SearchClient(engines[0])
        self.right = SearchClient(engines[1])

    @staticmethod
    def parse_docs(line):
        """
        format: timing count docs
        e.g. 8823 2 34 32
        """
        parts = line.split(' ')
        n = int(parts[1])
        if n == 0:
            return []
        docs = parts[2:]
        assert n == len(docs), "invalid record"
        return list(map(lambda x: int(x), docs))

    def compare(self, query: str, top_n: int):
        command: str = "TOP_N_DOCS\t{q}\t{n}\n".format(q=query, n=top_n)
        # print(command)
        docs_left = self.parse_docs(self.left.run_command(command))
        docs_right = self.parse_docs(self.right.run_command(command))
        n = max(len(docs_left), len(docs_right))

        if n == 0:
            return 1.0

        overlap = set(docs_left).intersection(set(docs_right))
        return len(overlap) / float(n)

def stats(numbers):
    xs = sorted(numbers)
    for i in range(0, 100, 5):
        print(f"p{i:03}:\t{xs[math.floor(len(xs) * i / 100)]:.2f}")
    print(f"p100:\t{xs[-1]:.2f}")
    print(f"mean:\t{functools.reduce(lambda x,y: x+y, xs, 0) / len(xs):.2f}")


if __name__ == "__main__":
    assert len(sys.argv) == 4
    query_file = sys.argv[1]
    client = OverlapClient(sys.argv[2:])

    num_identical = 0
    n = 0
    results = []
    low_oeverlaps = []
    with open(query_file, "r") as f:
        for line in f:
            parsed = json.loads(line)
            query = parsed['query']
            overlap = client.compare(query, 100)
            results.append(overlap)
            if overlap <= 0.95:
                low_oeverlaps.extend((overlap, query, parsed['tags']))

    stats(results)
    print("Low overlap queries:")
    for x in low_oeverlaps:
        print(x)



