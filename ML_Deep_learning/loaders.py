import json
from datetime import datetime
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor
from items import Item

CHUNK_SIZE = 1000
MIN_PRICE = 0.5
MAX_PRICE = 999.49

class ItemLoader:
    def __init__(self, name):
        self.name = name
        self.dataset = None

    def from_datapoint(self, datapoint):
        try:
            price_str = datapoint.get('price')
            if price_str:
                price = float(price_str)
                if MIN_PRICE <= price <= MAX_PRICE:
                    item = Item(datapoint, price)
                    return item if item.include else None
        except ValueError:
            return None

    def from_chunk(self, chunk):
        return [self.from_datapoint(dp) for dp in chunk if self.from_datapoint(dp)]

    def chunk_generator(self):
        size = len(self.dataset)
        for i in range(0, size, CHUNK_SIZE):
            yield self.dataset[i:i + CHUNK_SIZE]

    def load_in_parallel(self, workers):
        results = []
        chunk_count = (len(self.dataset) // CHUNK_SIZE) + 1
        with ProcessPoolExecutor(max_workers=workers) as pool:
            for batch in tqdm(pool.map(self.from_chunk, self.chunk_generator()), total=chunk_count):
                results.extend(batch)
        for result in results:
            result.category = self.name
        return results

    def load(self, path="data/meta_Appliances.jsonl", workers=8):
        start = datetime.now()
        print(f"Loading local dataset {self.name}...", flush=True)

        with open(path, 'r', encoding='utf-8') as f:
            # ⚠️ LIMIT to only 200 rows
            self.dataset = [json.loads(line.strip()) for _, line in zip(range(200), f)]

        results = self.load_in_parallel(workers)
        finish = datetime.now()
        print(f"Completed {self.name} with {len(results):,} items in {(finish-start).total_seconds()/60:.1f} mins", flush=True)
        return results
