import pandas as pd
import backend
import math

R = 8.314

def handle_sfc_file(file_name):

    sfc_entries = pd.read_csv(file_name)

    total_rows = sfc_entries.shape[0]

    total_values = 16  # Assuming you have 16 values in each row

    final_sfc = [0] * total_values

    for row_index in range(total_rows):
        refID = sfc_entries.iloc[row_index, 0]
        sfc_percent = sfc_entries.iloc[row_index, 1]

        # print("\n",refID)
        # print(sfc_percent)

        if refID.startswith("beta prime "):
            polymorph = "beta prime"
            TAG = refID.split("beta prime ")[-1]
        elif "beta" in refID:
            polymorph, TAG = refID.split()
        else:
            polymorph = "alpha"
            TAG = refID.split()[-1]

        symbol1, symbol2, symbol3 = TAG[:1], TAG[1:2], TAG[2:3]

        polym, tag, chemical_formula, mol_weight_sample, exp_enthalpy, exp_temp, sat_enthalpy_sample, temp_sample_a, temp_sample_b, hfGCM, tfGCM = backend.compute(
            symbol1, symbol2, symbol3, polymorph, "reference")

        # convert our values from C to K
        tag_enthalpy = sat_enthalpy_sample
        tag_tempK = temp_sample_a + 273.15

        # print(tag_enthalpy)
        # print(tag_tempK)

        # start calculation
        temp_i = 273.15

        for i in range(16):
            ln_i = (1000 * tag_enthalpy / R) * ((1 / temp_i) - (1 / tag_tempK))
            rounded_ln = round(ln_i, 4)

            exp_i = math.exp(ln_i)
            rounded_exp = round(exp_i, 6)

            sfc_percent_final = 1 * (exp_i * sfc_percent) / (1 + exp_i)
            sfc_rounded = round(sfc_percent_final, 4)

            # print(rounded_ln)
            # print(rounded_exp)
            # print(sfc_rounded)

            final_sfc[i] += sfc_rounded

            temp_i += 5
        # end

    # create array for T (degC)
    increment = 5
    length = 16

    degC = [i * increment for i in range(length)]

    # array for SFC (%)
    final_sfc = [round(value, 5) for value in final_sfc]

    # Print the final sum of values at each index
    # print("T (degC):")
    # print(degC)

    # print("SFC (%):")
    # print(final_sfc)

    # Create a dictionary with the data
    data = {
        "T (degC)": degC,
        "SFC (%)": final_sfc
    }

    # Create a DataFrame from the dictionary
    df = pd.DataFrame(data)

    # Specify the Excel file name
    excel_file = "sfc_output.xlsx"

    # Write the DataFrame to an Excel sheet
    df.to_excel(excel_file, index=False)

    return excel_file