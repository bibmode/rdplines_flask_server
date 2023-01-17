
from flask import Flask, flash, request, redirect, url_for
from multiprocessing import Process
import pandas as pd
import numpy as np
from rdp import rdp

app = Flask(__name__)

#simplify
@app.route('/api/simplify', methods = ['POST'])
def simplify_line():
    # get file from api call
    file = request.files['file']

    # read file using pandas
    df = pd.read_csv(file.stream, delimiter=',')

    # take the columns and rows
    cols = df.columns.values.tolist()
    first_row = df.iloc[:, 0]
    second_row = df.iloc[:, 1]

    # list rows
    list_row_1 = first_row.values.tolist()
    list_row_2 = second_row.values.tolist()

    def extract_val():
        first_row_rdp = [list_row_1[int(item[0])] for item in points_after_rdp]
        second_row_rdp = [item[1] for item in points_after_rdp]

        list_row_1_rdp = []
        list_row_2_rdp = []

        counter = 0
        for item in first_row:
            if item in first_row_rdp:
                list_row_1_rdp.append(item)
                list_row_2_rdp.append(second_row[counter])
            else:
                list_row_1_rdp.append(None)
                list_row_2_rdp.append(None)
            counter += 1

        # row_2 = points before rdp
        # row_2_rdp = points after rdp with null values
        return_val = {
            "columns": cols,
            "row_1": list_row_1,
            "row_2": list_row_2,
            "row_1_rdp": list_row_1_rdp,
            "row_2_rdp": list_row_2_rdp,
        }
        return return_val

    def ramer_douglas():
        points = np.column_stack([first_row.index, second_row])
        global points_after_rdp
        points_after_rdp = rdp(points, epsilon=3)
        return extract_val()

    return ramer_douglas()

#members api route
@app.route("/members")
def members():
    return {"members": ["Member1", "Member2", "Member3"]}


if __name__ == "__main__":
    app.run(debug=True)