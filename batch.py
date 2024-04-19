import pandas as pd
import backend

def handle_batch_file(file_name):

    batch_entries = pd.read_csv(file_name)

    total_rows = batch_entries.shape[0]

    results = []

    for row_index in range(total_rows):
        refID = batch_entries.iloc[row_index, 0]

        if refID.startswith("beta prime "):
            polymorph = "beta prime"
            TAG = refID.split("beta prime ")[-1]
        elif "beta" in refID:
            polymorph, TAG = refID.split()
        else:
            polymorph = "alpha"
            TAG = refID.split()[-1]

        symbol1, symbol2, symbol3 = TAG[:1], TAG[1:2], TAG[2:3]

        # print("Polym:", polymorph)
        # print("Symbol1:", symbol1)
        # print("Symbol2:", symbol2)
        # print("Symbol3:", symbol3)
        # print()

        polym, tag, chemical_formula, mol_weight_sample, exp_enthalpy, exp_temp, sat_enthalpy_sample, temp_sample_a, temp_sample_b, hfGCM, tfGCM = backend.compute(
            symbol1, symbol2, symbol3, polymorph, "reference")
        
        polym, tag, chemical_formula, mol_weight_sample, exp_enthalpy, exp_temp, sat_enthalpy_sample_P1L, temp_sample_a_P1L, temp_sample_b_P1L, hfGCM, tfGCM = backend.compute(
            symbol1, symbol2, symbol3, polymorph, "P1L")
        
        refID = polym + " " + tag
        
        results.append([refID, chemical_formula, mol_weight_sample, exp_enthalpy,
                        exp_temp, sat_enthalpy_sample, temp_sample_a, temp_sample_b, sat_enthalpy_sample_P1L, temp_sample_a_P1L, temp_sample_b_P1L, hfGCM, tfGCM])

    # convert the results list into a new DataFrame
    columns = ["Reference ID", "Molecular Formula", "Molar Mass", "Enthalpy", "Temperature",
            "Predicted Enthalpy (original)", "Predicted Temperature A (original)", "Predicted Temperature B (original)",
            "Predicted Enthalpy (updated)", "Predicted Temperature A (updated)", "Predicted Temperature B (updated)", "Enthalpy GC Method", "Temperature GC Method"]

    results_df = pd.DataFrame(results, columns=columns)

    # write the DataFrame to an Excel file with formatting
    output_file = "computed_data.xlsx"  # Change the file extension to .xlsx
    with pd.ExcelWriter(output_file, engine="xlsxwriter") as writer:
        results_df.to_excel(writer, index=False, sheet_name="Computed Data")

        # access the XlsxWriter workbook and worksheet objects for formatting
        workbook = writer.book
        worksheet = writer.sheets["Computed Data"]

        # customize column widths
        worksheet.set_column("A:A", 12)
        worksheet.set_column("B:B", 17)
        worksheet.set_column("C:C", 11)
        worksheet.set_column("D:D", 8)
        worksheet.set_column("E:E", 26)
        worksheet.set_column("F:F", 32)
        worksheet.set_column("G:G", 32)
        worksheet.set_column("H:H", 32)
        worksheet.set_column("I:I", 27)
        worksheet.set_column("J:J", 32.57)
        worksheet.set_column("K:K", 32.57)
        worksheet.set_column("L:L", 18.86)
        worksheet.set_column("M:M", 23)

    return output_file
