import numpy as np


def combine_taggers(decs, omegas):
    # Tagger combination algorithm (Internal function)
    p_b    = np.array([np.prod((1 + di) / 2 - di * (1 - omegai)) for di, omegai in zip(decs, omegas)])
    p_bbar = np.array([np.prod((1 - di) / 2 + di * (1 - omegai)) for di, omegai in zip(decs, omegas)])

    P_b = p_b / (p_b + p_bbar)

    dec_minus = P_b > 1 - P_b
    dec_plus  = P_b < 1 - P_b

    d_combined = np.zeros(len(decs))
    d_combined[dec_minus] = -1
    d_combined[dec_plus]  = +1

    omega_combined = 0.5 * np.ones(len(decs))
    omega_combined[dec_minus] = 1 - P_b[dec_minus]
    omega_combined[dec_plus]  = P_b[dec_plus]

    return d_combined, omega_combined
