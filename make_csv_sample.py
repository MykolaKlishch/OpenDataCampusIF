"""Produces evenly spaced sample from csv file
by leaving only each n-th row. Works well with
data_for_each_vehicle.csv but for other datasets
randomized sampling may be better choice than this tool
"""

import csv


def main():
    with open("data_for_each_vehicle.csv", mode="rt", encoding="utf-8"
              ) as fh_csv_in, open(
          "speed_each_vehicle_sample.csv", mode="wt", encoding="utf-8",
            newline="") as fh_csv_out:
        n = int(input("Each n-th row will be saved; n = "))
        reader = csv.reader(fh_csv_in)
        writer = csv.writer(fh_csv_out)
        for row_number, row in enumerate(reader):
            if row_number % n == 0:
                writer.writerow(row)


if __name__ == "__main__":
    main()



