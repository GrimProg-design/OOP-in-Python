import time

class SortStrategy:
    def sort(slef, data):
        raise NotImplementedError('Этот метод реализуется в наследниках')

class BubbleSortStrategy(SortStrategy):
    def sort(self, data):
        arr = data[:]
        comparisons = 0
        swaps = 0
        start = time.time()

        for i in range(len(arr)):
            for j in range(len(arr) - i - 1):
                comparisons += 1
                if arr[j] > arr[j + 1]:
                    swaps += 1
                    arr[j], arr[j+1] = arr[j+1], arr[j]
        
        return arr, {
            "algorithm": "BubbleSort",
            "comparisons": comparisons,
            "swaps": swaps,
            "time": time.time() - start
        }

class QuickSortStrategy(SortStrategy):
    def sort(self, data):
        arr = data[:]
        stats = {"comparisons": 0}
        start = time.time()

        def quick(lst):
            if len(lst) <= 1:
                return lst

            pivot = lst[len(lst)//2]
            left = [x for x in lst if x < pivot]
            mid  = [x for x in lst if x == pivot]
            right = [x for x in lst if x > pivot]
            stats["comparisons"] += len(lst)

            return quick(left) + mid + quick(right)

        result = quick(arr)
        stats["algorithm"] = "QuickSort"
        stats["time"] = time.time() - start
        return result, stats

class MergeSortStrategy(SortStrategy):
    def sort(self, data):
        arr = data[:]
        stats = {"comparisons": 0}
        start = time.time()

        def merge_sort(lst):
            if len(lst) <= 1:
                return lst
            
            mid = len(lst)//2
            left = merge_sort(lst[:mid])
            right = merge_sort(lst[mid:])
            return merge(left, right)
        
        def merge(a, b):
            res = []
            i = j =0
            while i < len(a) and j < len(b):
                stats["comparisons"] += 1
                if a[i] < b[j]:
                    res.append(a[i]); i+=1
                else:
                    res.append(b[j]); j+=1
            return res + a[i:] + b[j:]
        
        result = merge_sort(arr)
        stats["algorithm"] = "MergeSort"
        stats["time"] = time.time() - start
        return result, stats

class InsertionSortStrategy(SortStrategy):
    def sort(self, data):
        arr = data[:]
        swaps = 0
        comparisons = 0
        start = time.time()

        for i in range(1, len(arr)):
            key = arr[i]
            j = i-1
            while j >= 0 and arr[j] > key:
                comparisons += 1
                arr[j+1] = arr[j]
                swaps += 1
                j -= 1
            arr[j+1] = key

        return arr, {
            "algorithm": "InsertionSort",
            "comparisons": comparisons,
            "swaps": swaps,
            "time": time.time() - start
        }

class SmartSortStrategy(SortStrategy):
    def sort(self, data):
        disorder = 0
        for i in range(len(data)-1):
            if data[i] > data[i+1]:
                disorder += 1

        ratio = disorder / max(1, len(data)-1)

        if len(data) < 10:
            strategy = BubbleSortStrategy()
        elif ratio < 0.1:
            strategy = InsertionSortStrategy()
        else:
            strategy = QuickSortStrategy()

        return strategy.sort(data)

class DataSorter:
    def __init__(self, strategy, data):
        self.strategy = strategy
        self.data = data
        self.statistics = None

    def set_strategy(self, strategy):
        self.strategy = strategy

    def sort(self):
        result, stats = self.strategy.sort(self.data)
        self.statistics = stats
        return result

    def compare_strategies(self):
        strategies = [
            BubbleSortStrategy(),
            QuickSortStrategy(),
            MergeSortStrategy(),
            SmartSortStrategy()
        ]

        results = {}
        for s in strategies:
            _, info = s.sort(self.data)
            results[info["algorithm"]] = info["time"]
        return results

    def get_statistics(self):
        return self.statistics

    def __call__(self):
        return self.sort()
    
data = [5,3,8,1,4,7,2,6]

sorter = DataSorter(SmartSortStrategy(), data)

print("Результат:", sorter())
print("Статистика:", sorter.get_statistics())
print("Сравнение:", sorter.compare_strategies())