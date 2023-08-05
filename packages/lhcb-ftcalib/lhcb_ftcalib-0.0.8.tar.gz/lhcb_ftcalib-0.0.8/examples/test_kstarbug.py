import os
import matplotlib.pyplot as plt
import uproot
import matplotlib as mpl
mpl.rc('text', usetex=True)

import lhcb_ftcalib as ft

F = uproot.open("JPSIKSTAR.root")["DecayTree"]
print("Loading data")
print(F.keys())

df = F.arrays(filter_name=["*ETA", "*DEC", "*ID", "*TAU", "*TAUERR", "SW*"], library="pd")

tau_ps = df.B_TAU * 1000
outdir = "plots_Bd_data"
os.mkdir(outdir)

f = ft.PolynomialCalibration(2, ft.link.logit)

SStaggers = ft.TaggerCollection()
SStaggers.create_tagger("SSp",   df.B_SSProton_TAGETA,         df.B_SSProton_TAGDEC,         df.B_ID, "Bd", weight=df.SWeight, tau_ps=tau_ps)
SStaggers.create_tagger("SSpi",  df.B_SSPion_TAGETA,           df.B_SSPion_TAGDEC,           df.B_ID, "Bd", weight=df.SWeight, tau_ps=tau_ps)

OStaggers = ft.TaggerCollection()
OStaggers.create_tagger("IFT",   df.IFT_TAGETA,                df.IFT_TAGDEC,                df.B_ID, "Bd", weight=df.SWeight, tau_ps=tau_ps)
OStaggers.create_tagger("VtxCh", df.B_OSVtxCh_TAGETA,          df.B_OSVtxCh_TAGDEC,          df.B_ID, "Bd", weight=df.SWeight, tau_ps=tau_ps)
OStaggers.create_tagger("OSe",   df.B_OSElectronLatest_TAGETA, df.B_OSElectronLatest_TAGDEC, df.B_ID, "Bd", weight=df.SWeight, tau_ps=tau_ps)
OStaggers.create_tagger("OSmu",  df.B_OSMuonLatest_TAGETA,     df.B_OSMuonLatest_TAGDEC,     df.B_ID, "Bd", weight=df.SWeight, tau_ps=tau_ps)
OStaggers.create_tagger("OSk",   df.B_OSKaonLatest_TAGETA,     df.B_OSKaonLatest_TAGDEC,     df.B_ID, "Bd", weight=df.SWeight, tau_ps=tau_ps)
OStaggers.create_tagger("OSc",   df.B_OSCharm_TAGETA,          df.B_OSCharm_TAGDEC,          df.B_ID, "Bd", weight=df.SWeight, tau_ps=tau_ps)

# OStaggers.set_calibration(f)

SStaggers.calibrate()
OStaggers.calibrate()
OStaggers.plot_calibration_curves(savepath=outdir)

# IFT = ft.Tagger("IFT", df.IFT_TAGETA, df.IFT_TAGDEC, df.B_ID, weight=df.SWeight, mode="Bd", tau_ps=tau_ps, selection=df.SWeight>0)
# IFT.calibrate()
# ft.draw_calibration_curve(IFT, savepath=outdir)
