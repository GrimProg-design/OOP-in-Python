class SortStrategy:
    def sort(data):
        pass

class BubbleSortStrategy(SortStrategy):
    pass

class QuickSortStrategy(SortStrategy):
    pass

class MergeSortStrategy(SortStrategy):
    pass

class SmartSortStrategy(SortStrategy):
    pass

class DataSorter:
    def __init__(self, strategy, data, statistics):
        self.strategy = strategy
        self.data = data
        self.statistics = statistics

    def set_strategy(strategy):
        pass

    def sort():
        pass

    def compare_strategies():
        pass

    def get_statistics():
        pass

    def __call__():
        pass


data = [12, 6, 4, 3, 8]
for i in range(5 - 1):
    for j in range(5 - 1 - i):
        if data[j] > data[j+1]:
            data[j], data[j+1] = data[j+1], data[j]
print(data)