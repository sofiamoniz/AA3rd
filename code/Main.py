from Counters.Exact_counter import Exact_counter
from Counters.count_min_sketch import CountMinSketch
from tabulate import tabulate
from collections import defaultdict

def main(file_to_read):
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
    #columns = [50,40,20,30,10]
    #rows = [5,4,3,2,1]
    columns=[50,40]
    rows=[5,4]
    for col in columns:
        for row in rows:
            min_sketch = CountMinSketch(file_to_read, m=col, d=row)
            hash_functions = ['md5', 'sha256', 'sha1', 'blake2s', 'dsaEncryption']
            #print("col ", col," row ",row)
            for hash_func in hash_functions:
                #print("hash ", hash_func)
                min_sketch.count_chars(exact_counter_result, hash_function=hash_func)
                min_sketch_result = min_sketch.get_top_20_chars()
                #print(min_sketch_result)
                #print(min_sketch.get_total_counted_chars())
                tmp = str(col)+" "+str(row)
                rows_columns[tmp].append(min_sketch.get_total_counted_chars())
                min_sketch.clear()
    #print(rows_columns)
    for col_row, counting in rows_columns.items():
        table_rows.append([col_row.split()[0],col_row.split()[1], counting[0], counting[1], counting[2], counting[3], counting[4]])
    #print(tabulate(table_rows, headers=headers))
    file_name = file_to_read.split("/")[1].split(".")[0]
    with open("Results/counting_table_"+file_name+".txt","w") as output:
        output.write("\t\t\t\tCounting for file "+ file_name)
        output.write("\n\n\t\t\t\tExact counting: "+ str(exact_counter.get_total_counted_chars())+"\n\n")
        output.write(tabulate(table_rows,headers=headers))
    print("Done!")

if __name__ == '__main__':
    main("TextFiles/eng_hamlet.txt")