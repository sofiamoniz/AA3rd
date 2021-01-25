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
    exact_counter.write_top_20_chars("Results/exact_counter_eng_top_20_chars.txt")

    ###################
    # Create count min sketch #
    ###################
    headers = ['Colums','Rows','md5', 'sha256', 'sha1', 'blake2s', 'dsaEncryption']
    table_rows = []
    rows_columns = defaultdict(list)
    execution_time_dict = defaultdict(list)
    top_20_dict = {}
    columns = [50,40,20,30,10]
    rows = [5,4,3,2,1]
    print("Counting...")
    for col in columns:
        for row in rows:
            min_sketch = CountMinSketch(file_to_read, m=col, d=row)
            hash_functions = ['md5', 'sha256', 'sha1', 'blake2s', 'dsaEncryption']
            if len(hash_functions) == 5:
                for hash_func in hash_functions:
                    start_time = time.time()
                    min_sketch.count_chars(exact_counter_result, hash_function=hash_func)
                    execution_time = time.time() - start_time
                    min_sketch_top_20 = min_sketch.get_top_20_chars()
                    tmp = str(col)+" "+str(row)
                    if col == 50 and row == 5:
                        top_20_dict[hash_func]=min_sketch_top_20
                    rows_columns[tmp].append(min_sketch.get_total_counted_chars())
                    execution_time_dict[tmp].append(execution_time)
                    min_sketch.clear()
            else:
                print("INVALID HASH FUNCTIONS "+str(hash_functions)+" !")
                print("Please use ['md5', 'sha256', 'sha1', 'blake2s', 'dsaEncryption']")
                sys.exit()

    for col_row, counting in rows_columns.items():
        table_rows.append([col_row.split()[0],col_row.split()[1], counting[0], counting[1], counting[2], counting[3], counting[4]])
 

    table_execution_rows = []
    for col_row, exec_time in execution_time_dict.items():
        table_execution_rows.append([col_row.split()[0],col_row.split()[1], exec_time[0], exec_time[1], exec_time[2], exec_time[3], exec_time[4]])

    print("Wrinting results to files...")
    file_name = sys.argv[1]
    with open("Results/counting_table_"+file_name,"w") as output:
        output.write("\t\t\t\tCounting for file "+ file_name)
        output.write("\n\n\t\t\t\tExact counting: "+ str(exact_counter.get_total_counted_chars())+"\n\n")
        output.write(tabulate(table_rows,headers=headers))

    with open("Results/execution_times_"+file_name,"w") as output_execution:
        output_execution.write("\t\t\t\tExecution times (in seconds) for file "+ file_name+"\n\n")
        output_execution.write(tabulate(table_execution_rows, headers=headers))
    
    top_20_rows=[]
    top_20_headers = ["Hash function", "Count min sketch top 20", "Count min sketch counting"]
    for hash_func, counting in top_20_dict.items():
        for c in counting:
            top_20_rows.append([hash_func, c[0], c[1]])
    with open("Results/top_20_" + file_name, "w") as output_top_20:
        output_top_20.write("\t\t\t\tTop 20, with 50 columns and 5 rows, for file "+ file_name+"\n\n")
        output_top_20.write(tabulate(top_20_rows, headers=top_20_headers))
    print("Done!")

if __name__ == '__main__':
    main()