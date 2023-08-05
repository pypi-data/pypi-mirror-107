import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def distribution_mistag(N, dist="normal", mean=0.25):
    if dist == "normal":
        return np.clip(np.random.normal(loc=mean, scale=0.05, size=N), 0, 0.5)


def toy_data(N, calib, params, osc, dist_centers, life=1.52, DM=0.5065, DG=0, Aprod=0):
    """ Toy data generator """
    np.random.seed(2387465)
    # Generate decay time
    if osc:
        tau = np.random.exponential(scale = 1.0 / life, size=N)
        # tau_choose  = np.random.uniform(0, 1, N)
        # tau = tau[tau_choose < 2 * np.arctan(2 * tau) / np.pi]

        N = len(tau)

    toydata = pd.DataFrame({
        "eventNumber" : np.arange(N),
        "TOY_PROD"    : np.ones(N, dtype=np.int32),
        "TOY_DECAY"   : np.ones(N, dtype=np.int32),
    })
    toydata.TOY_PROD.loc[N // 2:] *= -1
    toydata.TOY_DECAY.loc[N // 2:] *= -1

    if osc:
        # Oscillate mesons
        toydata["TAU"] = tau
        Amix = np.cos(DM * toydata.TAU) / np.cosh(0.5 * DG * toydata.TAU)
        osc_prob = 0.5 * (1 - Amix)
        rand_thresh = np.random.uniform(0, 1, N)
        has_oscillated = rand_thresh < osc_prob
        toydata.loc[has_oscillated, "TOY_DECAY"] *= -1
        toydata["OSC"] = has_oscillated

    for t, tparams in enumerate(params):
        name = f"TOY{t}"
        toydata[f"{name}_DEC"] = np.ones(N, dtype=np.int32)
        toydata[f"{name}_DEC"].loc[N // 2:] *= -1
        toydata[f"{name}_OMEGA"] = distribution_mistag(N, "normal", mean=dist_centers[t])

    for t, tparams in enumerate(params):
        name = f"TOY{t}"
        average_omega = np.mean(toydata[f"{name}_OMEGA"])  # must assume that <omega> is approximately <eta>

        # Compute tagging decision from omega
        rand_thresh = np.random.uniform(0, 1, N)
        toydata.loc[rand_thresh < toydata[f"{name}_OMEGA"], f"{name}_DEC"] *= -1

        # Compute true inverse omegas to get eta distributions
        inv_prec = 1000
        eta_lin = np.linspace(0, 0.5, inv_prec)
        omegaP_lineshape = calib.eval(tparams, eta_lin,  np.ones(inv_prec), average_omega)
        omegaM_lineshape = calib.eval(tparams, eta_lin, -np.ones(inv_prec), average_omega)
        toydata.loc[toydata["TOY_DECAY"] ==  1, f"{name}_ETA"] = np.interp(toydata[toydata["TOY_DECAY"] ==  1][f"{name}_OMEGA"], omegaP_lineshape, eta_lin)
        toydata.loc[toydata["TOY_DECAY"] == -1, f"{name}_ETA"] = np.interp(toydata[toydata["TOY_DECAY"] == -1][f"{name}_OMEGA"], omegaM_lineshape, eta_lin)

    # Shuffle
    toydata = toydata.sample(frac=1)

    return toydata
