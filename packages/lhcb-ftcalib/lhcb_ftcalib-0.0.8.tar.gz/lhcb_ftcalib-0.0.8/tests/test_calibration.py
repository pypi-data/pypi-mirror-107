import os
import numpy as np
import uproot
from toy_tagger import toy_data
import lhcb_ftcalib as ft
import root_pandas as rp


def delete_file(F):
    if os.path.exists(F):
        os.remove(F)
        print("Removed", F)


def test_prepare_tests():
    if not os.path.exists("tests/calib"):
        os.mkdir("tests/calib")

    if not os.path.exists("tests/calib/toy_data.root"):
        poly1 = ft.PolynomialCalibration(2, ft.link.mistag)
        toydata = toy_data(30000, poly1, [[0, 1, 0, 1],
                                          [0.01, 1.3, 0.01, 1],
                                          [0.01, 1, 0.01, 1.3]],
                                          dist_centers=[0.25, 0.3, 0.42],
                                          osc=False)
        rp.to_root(toydata, "tests/calib/toy_data.root", key="BU_TOY", store_index=False)

        toydata = toy_data(30000, poly1, [[0, 1, 0, 1],
                                          [0.01, 1.3, 0.01, 1],
                                          [0.01, 1, 0.01, 1.3]],
                                          dist_centers=[0.25, 0.3, 0.42],
                                          osc=True)
        rp.to_root(toydata, "tests/calib/toy_data.root", key="BD_TOY", mode="a", store_index=False)


def compare_dataframe_to_file(filename, key, df):
    assert os.path.exists(filename)
    fdata = uproot.open(filename)[key].arrays(library="pd")
    for branch in fdata.columns.values:
        if branch in df:
            print(f"Comparing branch {branch} ...")
            b1 = np.array(fdata[branch])
            b2 = np.array(df[branch])
            if not all(np.isclose(b1, b2)):
                print("FAIL")
                print("CLI ", b1[b1 != b2])
                print("API ", b2[b1 != b2])
                raise AssertionError
            print("PASSED")


def test_run_calibrate_Bu():
    # Run CLI command without crashing, then do the same with the API and compare results
    # CLI
    testfile = "tests/calib/test_calibrate_Bu"
    delete_file(testfile + ".json")
    F = "tests/calib/toy_data.root"

    df = uproot.open(F)["BU_TOY"].arrays(["TOY0_ETA", "TOY1_ETA", "TOY2_ETA",
                                          "TOY0_DEC", "TOY1_DEC", "TOY2_DEC", "TOY_DECAY"], library="pd")
    tc = ft.TaggerCollection()
    tc.create_tagger("TOY0", df.TOY0_ETA, df.TOY0_DEC, B_ID=df.TOY_DECAY, mode="Bu")
    tc.create_tagger("TOY1", df.TOY1_ETA, df.TOY1_DEC, B_ID=df.TOY_DECAY, mode="Bu")
    tc.create_tagger("TOY2", df.TOY2_ETA, df.TOY2_DEC, B_ID=df.TOY_DECAY, mode="Bu")
    tc.calibrate()
    apidata = tc.get_dataframe(calibrated=True)

    delete_file(testfile + ".json")


def test_run_calibrate_combine_Bu():
    # Run CLI command without crashing, then do the same with the API and compare results
    # CLI
    testfile = "tests/calib/test_calibrate_combine_Bu"
    delete_file(testfile + ".json")
    F = "tests/calib/toy_data.root"

    df = uproot.open(F)["BU_TOY"].arrays(["TOY0_ETA", "TOY1_ETA", "TOY2_ETA",
                                          "TOY0_DEC", "TOY1_DEC", "TOY2_DEC", "TOY_DECAY"], library="pd")
    tc = ft.TaggerCollection()
    tc.create_tagger("TOY0", df.TOY0_ETA, df.TOY0_DEC, B_ID=df.TOY_DECAY, mode="Bu")
    tc.create_tagger("TOY1", df.TOY1_ETA, df.TOY1_DEC, B_ID=df.TOY_DECAY, mode="Bu")
    tc.create_tagger("TOY2", df.TOY2_ETA, df.TOY2_DEC, B_ID=df.TOY_DECAY, mode="Bu")
    tc.calibrate()
    apidata = tc.get_dataframe(calibrated=True)
    combination = tc.combine_taggers("Combination", calibrated=True)
    combdata = combination.get_dataframe(calibrated=False)
    for v in combdata.columns.values:
        apidata[v] = combdata[v]

    delete_file(testfile + ".json")


def test_run_calibrate_combine_calibrate_Bu():
    # Run CLI command without crashing, then do the same with the API and compare results
    # CLI
    testfile = "tests/calib/test_calibrate_combine_calibrate_Bu"
    delete_file(testfile + ".json")
    F = "tests/calib/toy_data.root"

    df = uproot.open(F)["BU_TOY"].arrays(["TOY0_ETA", "TOY1_ETA", "TOY2_ETA",
                                          "TOY0_DEC", "TOY1_DEC", "TOY2_DEC", "TOY_DECAY"], library="pd")
    tc = ft.TaggerCollection()
    tc.create_tagger("TOY0", df.TOY0_ETA, df.TOY0_DEC, B_ID=df.TOY_DECAY, mode="Bu")
    tc.create_tagger("TOY1", df.TOY1_ETA, df.TOY1_DEC, B_ID=df.TOY_DECAY, mode="Bu")
    tc.create_tagger("TOY2", df.TOY2_ETA, df.TOY2_DEC, B_ID=df.TOY_DECAY, mode="Bu")
    tc.calibrate()
    apidata = tc.get_dataframe(calibrated=True)
    combination = tc.combine_taggers("Combination", calibrated=True)
    combination.calibrate(ignore_eta_out_of_range=False)
    combdata = combination.get_dataframe(calibrated=False)
    combdata_calib = combination.get_dataframe(calibrated=True)
    for v in combdata.columns.values:
        apidata[v] = combdata[v]
    for v in combdata_calib.columns.values:
        apidata[v] = combdata_calib[v]

    delete_file(testfile + ".json")


def test_run_calibrate_Bd():
    # Run CLI command without crashing, then do the same with the API and compare results
    # CLI
    testfile = "tests/calib/test_calibrate_Bd"
    delete_file(testfile + ".json")
    F = "tests/calib/toy_data.root"

    df = uproot.open(F)["BD_TOY"].arrays(["TOY0_ETA", "TOY1_ETA", "TOY2_ETA",
                                          "TOY0_DEC", "TOY1_DEC", "TOY2_DEC", "TOY_DECAY", "TAU"], library="pd")
    tc = ft.TaggerCollection()
    tc.create_tagger("TOY0", df.TOY0_ETA, df.TOY0_DEC, B_ID=df.TOY_DECAY, mode="Bd", tau_ps=df.TAU)
    tc.create_tagger("TOY1", df.TOY1_ETA, df.TOY1_DEC, B_ID=df.TOY_DECAY, mode="Bd", tau_ps=df.TAU)
    tc.create_tagger("TOY2", df.TOY2_ETA, df.TOY2_DEC, B_ID=df.TOY_DECAY, mode="Bd", tau_ps=df.TAU)
    tc.calibrate()
    apidata = tc.get_dataframe()

    delete_file(testfile + ".json")


def test_run_calibrate_Bd_selection_vartype1():
    # Run CLI command without crashing, then do the same with the API and compare results
    # CLI
    testfile = "tests/calib/test_calibrate_Bd_sel_v1"
    delete_file(testfile + ".json")
    F = "tests/calib/toy_data.root"

    df = uproot.open(F)["BD_TOY"].arrays(["TOY0_ETA", "TOY1_ETA", "TOY2_ETA",
                                          "TOY0_DEC", "TOY1_DEC", "TOY2_DEC", "TOY_DECAY", "TAU"], library="pd")
    selection = df.TAU > 0.5
    tc = ft.TaggerCollection()
    tc.create_tagger("TOY0", df.TOY0_ETA, df.TOY0_DEC, B_ID=df.TOY_DECAY, mode="Bd", tau_ps=df.TAU, selection=selection)
    tc.create_tagger("TOY1", df.TOY1_ETA, df.TOY1_DEC, B_ID=df.TOY_DECAY, mode="Bd", tau_ps=df.TAU, selection=selection)
    tc.create_tagger("TOY2", df.TOY2_ETA, df.TOY2_DEC, B_ID=df.TOY_DECAY, mode="Bd", tau_ps=df.TAU, selection=selection)
    tc.calibrate()
    apidata = tc.get_dataframe()

    delete_file(testfile + ".json")


def test_run_calibrate_Bd_selection_vartype2():
    # Run CLI command without crashing, then do the same with the API and compare results
    # CLI
    # import pudb
    # pu.db
    testfile = "tests/calib/test_calibrate_Bd_sel_v2"
    delete_file(testfile + ".json")
    F = "tests/calib/toy_data.root"

    df = uproot.open(F)["BD_TOY"].arrays(["TOY0_ETA", "TOY1_ETA", "TOY2_ETA",
                                          "TOY0_DEC", "TOY1_DEC", "TOY2_DEC", "TOY_DECAY", "TAU", "eventNumber"], library="pd")
    selection = df.eventNumber % 2 == 0
    tc = ft.TaggerCollection()
    tc.create_tagger("TOY0", df.TOY0_ETA, df.TOY0_DEC, B_ID=df.TOY_DECAY, mode="Bd", tau_ps=df.TAU, selection=selection)
    tc.create_tagger("TOY1", df.TOY1_ETA, df.TOY1_DEC, B_ID=df.TOY_DECAY, mode="Bd", tau_ps=df.TAU, selection=selection)
    tc.create_tagger("TOY2", df.TOY2_ETA, df.TOY2_DEC, B_ID=df.TOY_DECAY, mode="Bd", tau_ps=df.TAU, selection=selection)
    tc.calibrate()
    apidata = tc.get_dataframe()

    delete_file(testfile + ".json")


def test_run_calibrate_combine_Bd():
    # Run CLI command without crashing, then do the same with the API and compare results
    # CLI
    testfile = "tests/calib/test_calibrate_combine_Bd"
    delete_file(testfile + ".json")
    F = "tests/calib/toy_data.root"

    df = uproot.open(F)["BD_TOY"].arrays(["TOY0_ETA", "TOY1_ETA", "TOY2_ETA",
                                          "TOY0_DEC", "TOY1_DEC", "TOY2_DEC", "TOY_DECAY", "TAU"], library="pd")
    tc = ft.TaggerCollection()
    tc.create_tagger("TOY0", df.TOY0_ETA, df.TOY0_DEC, B_ID=df.TOY_DECAY, mode="Bd", tau_ps=df.TAU)
    tc.create_tagger("TOY1", df.TOY1_ETA, df.TOY1_DEC, B_ID=df.TOY_DECAY, mode="Bd", tau_ps=df.TAU)
    tc.create_tagger("TOY2", df.TOY2_ETA, df.TOY2_DEC, B_ID=df.TOY_DECAY, mode="Bd", tau_ps=df.TAU)
    tc.calibrate()
    combination = tc.combine_taggers("Combination", calibrated=True)
    apidata = tc.get_dataframe(calibrated=True)
    combdata = combination.get_dataframe(calibrated=False)
    for v in combdata.columns.values:
        apidata[v] = combdata[v]

    delete_file(testfile + ".json")


def test_run_calibrate_combine_calibrate_Bd():
    # Run CLI command without crashing, then do the same with the API and compare results
    # CLI
    testfile = "tests/calib/test_calibrate_combine_calibrate_Bd"
    delete_file(testfile + ".json")
    F = "tests/calib/toy_data.root"

    df = uproot.open(F)["BD_TOY"].arrays(["TOY0_ETA", "TOY1_ETA", "TOY2_ETA",
                                          "TOY0_DEC", "TOY1_DEC", "TOY2_DEC", "TOY_DECAY", "TAU"], library="pd")
    tc = ft.TaggerCollection()
    tc.create_tagger("TOY0", df.TOY0_ETA, df.TOY0_DEC, B_ID=df.TOY_DECAY, mode="Bd", tau_ps=df.TAU)
    tc.create_tagger("TOY1", df.TOY1_ETA, df.TOY1_DEC, B_ID=df.TOY_DECAY, mode="Bd", tau_ps=df.TAU)
    tc.create_tagger("TOY2", df.TOY2_ETA, df.TOY2_DEC, B_ID=df.TOY_DECAY, mode="Bd", tau_ps=df.TAU)
    tc.calibrate()
    combination = tc.combine_taggers("Combination", calibrated=True)
    combination.calibrate()
    apidata = tc.get_dataframe(calibrated=True)
    combdata = combination.get_dataframe(calibrated=False)
    combdata_calib = combination.get_dataframe(calibrated=True)
    for v in combdata.columns.values:
        apidata[v] = combdata[v]
    for v in combdata_calib.columns.values:
        apidata[v] = combdata_calib[v]

    delete_file(testfile + ".json")


def test_run_calibrate_combine_calibrate_Bd_selection():
    # Run CLI command without crashing, then do the same with the API and compare results
    # CLI
    testfile = "tests/calib/test_calibrate_combine_calibrate_Bd_sel"
    delete_file(testfile + ".json")
    F = "tests/calib/toy_data.root"

    df = uproot.open(F)["BD_TOY"].arrays(["TOY0_ETA", "TOY1_ETA", "TOY2_ETA",
                                          "TOY0_DEC", "TOY1_DEC", "TOY2_DEC", "TOY_DECAY", "TAU", "eventNumber"], library="pd")

    selection = df.eventNumber % 2 == 0
    tc = ft.TaggerCollection()
    tc.create_tagger("TOY0", df.TOY0_ETA, df.TOY0_DEC, B_ID=df.TOY_DECAY, mode="Bd", tau_ps=df.TAU, selection=selection)
    tc.create_tagger("TOY1", df.TOY1_ETA, df.TOY1_DEC, B_ID=df.TOY_DECAY, mode="Bd", tau_ps=df.TAU, selection=selection)
    tc.create_tagger("TOY2", df.TOY2_ETA, df.TOY2_DEC, B_ID=df.TOY_DECAY, mode="Bd", tau_ps=df.TAU, selection=selection)
    tc.calibrate()
    combination = tc.combine_taggers("Combination", calibrated=True)
    combination.calibrate()
    apidata = tc.get_dataframe(calibrated=True)
    combdata = combination.get_dataframe(calibrated=False)
    combdata_calib = combination.get_dataframe(calibrated=True)
    for v in combdata.columns.values:
        apidata[v] = combdata[v]
    for v in combdata_calib.columns.values:
        apidata[v] = combdata_calib[v]

    delete_file(testfile + ".json")
