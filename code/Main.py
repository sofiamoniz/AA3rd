from Counters.Exact_counter import Exact_counter
from Counters.count_min_sketch import CountMinSketch

def main(file_to_read):
    ###################
    # Create exact counter #
    ###################
    exact_counter = Exact_counter(file_to_read)
    exact_counter.count_chars()
    exact_counter_result = exact_counter.get_final_counting()
    print(exact_counter.get_top_20_chars())
    print(exact_counter.get_total_counted_chars())
    #exact_counter.write_final_counting("Results/ExactCounter/ENG/final_counting.txt")
    #exact_counter.write_top_20_chars("Results/ExactCounter/ENG/eng_top_20_chars.txt")

    ###################
    # Create count min sketch #
    ###################
    columns = [50,40,20,30,10]
    rows = [5,4,3,2,1]
    for col in columns:
        for row in rows:
            min_sketch = CountMinSketch(file_to_read, m=col, d=row)
            hash_functions = ['md5', 'sha256', 'sha1', 'blake2s', 'dsaEncryption']
            print("col ", col," row ",row)
            for hash_func in hash_functions:
                print("hash ", hash_func)
                min_sketch.count_chars(exact_counter_result, hash_function=hash_func)
                min_sketch_result = min_sketch.get_top_20_chars()
                print(min_sketch_result)
                print(min_sketch.get_total_counted_chars())
                min_sketch.clear()


    

if __name__ == '__main__':
    main("TextFiles/eng_hamlet.txt")