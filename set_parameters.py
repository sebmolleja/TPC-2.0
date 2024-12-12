import pandas as pd

def sat_enthalpy_params(type, parseCol):

    sat_enthalpy_vars = pd.read_csv(
        "data/asmDB-SatAcidEnthalpyCoefficientEstimates.csv")

    sat_enthalpy_vars_P1L = pd.read_csv(
        "data/new_params/new_SatAcidEnthalpyP2L.csv")

    if type == "reference":
        h = sat_enthalpy_vars.iloc[1, parseCol]
        ho = sat_enthalpy_vars.iloc[0, parseCol]
        hxy = sat_enthalpy_vars.iloc[4, parseCol]

        s = sat_enthalpy_vars.iloc[3, parseCol]
        so = sat_enthalpy_vars.iloc[2, parseCol]
        sxy = sat_enthalpy_vars.iloc[5, parseCol]

        xo = sat_enthalpy_vars.iloc[7, parseCol]
        k = sat_enthalpy_vars.iloc[6, parseCol]

        temp_inf_a = sat_enthalpy_vars.iloc[8, parseCol]

    elif type == "P1L":
        h = sat_enthalpy_vars_P1L.iloc[1, parseCol]
        ho = sat_enthalpy_vars_P1L.iloc[0, parseCol]
        hxy = sat_enthalpy_vars_P1L.iloc[4, parseCol]

        s = sat_enthalpy_vars_P1L.iloc[3, parseCol]
        so = sat_enthalpy_vars_P1L.iloc[2, parseCol]
        sxy = sat_enthalpy_vars_P1L.iloc[5, parseCol]

        xo = sat_enthalpy_vars_P1L.iloc[7, parseCol]
        k = sat_enthalpy_vars_P1L.iloc[6, parseCol]

        temp_inf_a = sat_enthalpy_vars_P1L.iloc[8, parseCol]

    return h, ho, hxy, s, so, sxy, xo, k, temp_inf_a


def sat_temp_params(type, parseCol):

    sat_temp_vars = pd.read_csv(
        "data/asmDB-SatAcidTempCoefficientEstimates.csv")
    sat_temp_vars_P1L = pd.read_csv("data/new_params/new_SatAcidTempP2L.csv")

    Ao = sat_temp_vars.iloc[0, parseCol]
    Aodd = sat_temp_vars.iloc[1, parseCol]
    Ax = sat_temp_vars.iloc[2, parseCol]
    Ax2 = sat_temp_vars.iloc[3, parseCol]
    Axy = sat_temp_vars.iloc[4, parseCol]
    Ay = sat_temp_vars.iloc[5, parseCol]
    Ay2 = sat_temp_vars.iloc[6, parseCol]

    Bo = sat_temp_vars.iloc[7, parseCol]
    Bodd = sat_temp_vars.iloc[8, parseCol]
    Bx = sat_temp_vars.iloc[9, parseCol]
    Bx2 = sat_temp_vars.iloc[10, parseCol]
    Bxy = sat_temp_vars.iloc[11, parseCol]
    By = sat_temp_vars.iloc[12, parseCol]
    By2 = sat_temp_vars.iloc[13, parseCol]

    if type == "reference":
        temp_inf_b = sat_temp_vars.iloc[14, parseCol]
    elif type == "P1L":
        temp_inf_b = sat_temp_vars_P1L.iloc[14, parseCol]

    return Ao, Aodd,  Ax, Ax2, Axy, Ay, Ay2, Bo, Bodd, Bx, Bx2, Bxy, By, By2, temp_inf_b


def unsat_enthalpy_params(type, parseCol):

    unsat_enthalpy_vars = pd.read_csv(
        "data/asmDB-UnsatAcidEnthalpyCoefficientEstimates.csv")
    unsat_enthalpy_vars_P1L = pd.read_csv(
        "data/new_params/new_UnsatAcidEnthalpyP2L.csv")

    if type == "reference":
        hol = unsat_enthalpy_vars.iloc[0, parseCol]
        hel = unsat_enthalpy_vars.iloc[1, parseCol]
        hli = unsat_enthalpy_vars.iloc[2, parseCol]

    elif type == "P1L":
        hol = unsat_enthalpy_vars_P1L.iloc[0, parseCol]
        hel = unsat_enthalpy_vars_P1L.iloc[1, parseCol]
        hli = unsat_enthalpy_vars_P1L.iloc[2, parseCol]

    return hol, hel, hli


def unsat_temp_params(type, parseCol):

    unsat_temp_vars = pd.read_csv(
        "data/asmDB-UnsatAcidTempCoefficientEstimates.csv")
    unsat_temp_vars_P1L = pd.read_csv(
        "data/new_params/new_UnsatAcidTempP2L.csv")

    if type == "reference":
        aO = unsat_temp_vars.iloc[0, parseCol]
        aE = unsat_temp_vars.iloc[1, parseCol]
        aJ = unsat_temp_vars.iloc[2, parseCol]
        aN = unsat_temp_vars.iloc[3, parseCol]

        aOO = unsat_temp_vars.iloc[4, parseCol]
        aDD = unsat_temp_vars.iloc[5, parseCol]
        aJJ = unsat_temp_vars.iloc[6, parseCol]
        aNN = unsat_temp_vars.iloc[7, parseCol]

        aOJ = unsat_temp_vars.iloc[8, parseCol]
        aON = unsat_temp_vars.iloc[9, parseCol]
        aJN = unsat_temp_vars.iloc[10, parseCol]

        bO = unsat_temp_vars.iloc[11, parseCol]
        bJ = unsat_temp_vars.iloc[12, parseCol]
        bN = unsat_temp_vars.iloc[13, parseCol]

    elif type == "P1L":
        aO = unsat_temp_vars_P1L.iloc[0, parseCol]
        aE = unsat_temp_vars_P1L.iloc[1, parseCol]
        aJ = unsat_temp_vars_P1L.iloc[2, parseCol]
        aN = unsat_temp_vars_P1L.iloc[3, parseCol]

        aOO = unsat_temp_vars_P1L.iloc[4, parseCol]
        aDD = unsat_temp_vars_P1L.iloc[5, parseCol]
        aJJ = unsat_temp_vars_P1L.iloc[6, parseCol]
        aNN = unsat_temp_vars_P1L.iloc[7, parseCol]

        aOJ = unsat_temp_vars_P1L.iloc[8, parseCol]
        aON = unsat_temp_vars_P1L.iloc[9, parseCol]
        aJN = unsat_temp_vars_P1L.iloc[10, parseCol]

        bO = unsat_temp_vars_P1L.iloc[11, parseCol]
        bJ = unsat_temp_vars_P1L.iloc[12, parseCol]
        bN = unsat_temp_vars_P1L.iloc[13, parseCol]

    return aO, aE, aJ, aN, aOO, aDD, aJJ, aNN, aOJ, aON, aJN, bO, bJ, bN
