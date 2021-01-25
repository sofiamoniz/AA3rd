from Counters.Exact_counter import Exact_counter
from Counters.count_min_sketch import CountMinSketch
from tabulate import tabulate
from collections import defaultdict
import getopt, sys
import os.path
from os import path
import time

def main():
    
    if len(sys.argv)<2:
        print ("Usage:\n  Main.py <text file>")
        print ("\nExample:\n  Main.py eng_hamlet.txt")
        print("\nText file must be inside 'TextFiles' folder!")
        sys.exit()

    file_to_read = "TextFiles/"+sys.argv[1]

    if(path.exists(file_to_read) == False):
        print ("Usage:\n  Main.py <text file>")
        print ("\nExample:\n  Main.py eng_hamlet.txt")
        print("\nText file must be inside 'TextFiles' folder!")
        sys.exit()


    ###################
    # Create exact counter #
    ###################
    exact_counter = Exact_counter(file_to_read)
    exact_counter.count_chars()
    exact_counter_result = exact_counter.get_final_counting()
    #print(exact_counter.get_top_20_chars())
    #print(exact_counter.get_total_counted_chars())
    #exact_counter.write_final_counting("Results/ExactCounter/ENG/final_counting.txt")
    #exact_counter.write_top_20_chars("Results/ExactCounter/ENG/eng_top_20_chars.txt")

    ###################
    # Create count min sketch #
    ###################
    headers = ['Colums','Rows','md5', 'sha256', 'sha1', 'blake2s', 'dsaEncryption']
    table_rows = []
    rows_columns = defaultdict(list)
    execution_time_dict = defaultdict(list)
    top_20_dict = defaultdict(list)
    #columns = [50,40,20,30,10]
    #rows = [5,4,3,2,1]
    columns=[50,40]
    rows=[5,4]
    print("Counting...")
    for col in columns:
        for row in rows:
            min_sketch = CountMinSketch(file_to_read, m=col, d=row)
            hash_functions = ['md5', 'sha256', 'sha1', 'blake2s', 'dsaEncryption']
            for hash_func in hash_functions:
                start_time = time.time()
                min_sketch.count_chars(exact_counter_result, hash_function=hash_func)
                execution_time = time.time() - start_time
                min_sketch_top_20 = min_sketch.get_top_20_chars()
                tmp = str(col)+" "+str(row)
                top_20_dict[hash_func].append({tmp:min_sketch_top_20})
                rows_columns[tmp].append({hash_func:min_sketch.get_total_counted_chars()})
                #execution_time_dict[tmp].append(execution_time)
                min_sketch.clear()
    #print(rows_columns)
    #for rows_columns, hash_results in rows_columns.items():
        #print(rows_columns)
        #print(hash_results)
        #print(hash_results[md5])
    print(rows_columns)

    for col_row, counting in rows_columns.items():
        print([col_row.split()[0],col_row.split()[1], counting[0]['md5'], counting[1].values(), counting[2].values(), counting[3].values(), counting[4].values()])
    #print(tabulate(table_rows, headers=headers))

    """
    print("Wrinting results to files...")
    file_name = sys.argv[1]
    with open("Results/counting_table_"+file_name,"w") as output:
        output.write("\t\t\t\tCounting for file "+ file_name)
        output.write("\n\n\t\t\t\tExact counting: "+ str(exact_counter.get_total_counted_chars())+"\n\n")
        output.write(tabulate(table_rows,headers=headers))
    """

if __name__ == '__main__':
    main()