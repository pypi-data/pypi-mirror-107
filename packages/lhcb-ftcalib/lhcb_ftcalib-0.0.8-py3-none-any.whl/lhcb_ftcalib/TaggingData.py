import numpy as np
import pandas as pd

from lhcb_ftcalib.printing import raise_error, raise_warning
from lhcb_ftcalib.resolution_model import mixing_asymmetry


def get_absid(ID):
    ids = ID.abs().unique()
    ids = list(ids[ids != 0])
    raise_error(len(ids) > 0, f"There are no nonzero particle IDs in the ID branch {ids}")
    raise_error(len(ids) == 1, f"There are too many particle IDs in the ID branch: {ids}")
    raise_warning(ids[0] in (511, 521, 531), f"Particle ID {ids[0]} does not belong to a Bu, Bd or Bs meson")
    return ids[0]


class TaggingData:
    r"""
    TaggingData
    Type for keeping track of tagging data and basic event statistics

    :param eta_data: Uncalibrated mistags
    :type eta_data: list
    :param dec_data: Uncalibrated tagging decisions
    :type dec_data: list
    :param ID: B meson particle IDs
    :type ID: list
    :param tau: Decay time in picoseconds
    :type tau: list
    :param tauerr: Decay time uncertainty in picoseconds
    :type tauerr: list
    :param weights: Per-event weights
    :type weights: list
    :param ignore_out_of_range: Whether to ignore mistag values :math:`\eta\notin [0,0.5]` (not recommended)
    :type ignore_out_of_range: bool
    """
    def __init__(self, eta_data, dec_data, ID, tau, tauerr, weights, selection, ignore_eta_out_of_range=False):
        # Init full tagging data (Copy to avoid spooky action at a distance)
        self.all_eta    = pd.Series(eta_data, copy=True)                  #: All eta values
        self.all_dec    = pd.Series(dec_data, dtype=np.int32, copy=True)  #: All dec values
        self.all_B_ID   = pd.Series(ID, copy=True)                        #: All B meson IDs
        self.selected   = pd.Series(selection, copy=True)                 #: Mask of events in selection
        if tau is not None:
            self.all_tau = pd.Series(tau, copy=True)  #: All decay time values
        else:
            self.all_tau = None
        if tauerr is not None:
            self.all_tauerr = pd.Series(tauerr, copy=True)  #: All decay time uncertainty values
        else:
            self.all_tauerr = None

        # Reset indices so that from now on everything is guaranteed to be aligned
        # (pd.Series copy constructor preserves alignment)
        self.all_eta.reset_index(drop=True, inplace=True)
        self.all_dec.reset_index(drop=True, inplace=True)
        self.all_B_ID.reset_index(drop=True, inplace=True)
        self.selected.reset_index(drop=True, inplace=True)
        if self.all_tau is not None:
            self.all_tau.reset_index(drop=True, inplace=True)
        if self.all_tauerr is not None:
            self.all_tauerr.reset_index(drop=True, inplace=True)

        # Memorize which events are overflow
        self.overflow  = (self.all_eta > 0.5)  #: Mask of events with :math:`\omega>0.5`
        self.underflow = (self.all_eta < 0)    #: Mask of events with :math:`\omega<0`
        self.noverflow = self.overflow.sum()   #: Number of calibrated mistags > 0.5

        if not ignore_eta_out_of_range:
            # eta > 0.5 = untagged
            self.all_eta[self.overflow] = 0.5
            self.all_dec[self.overflow] = 0
            self.all_eta[self.underflow] = 0

        self.tagged     = self.all_dec != 0                                          #: Mask of tagged events
        self.tagged_sel = (self.all_dec != 0) & self.selected                        #: Mask of selected and tagged events

        # Initialize tagged statistics for faster access (at the cost of memory consumption)
        self.dec        = pd.Series(self.all_dec[self.tagged_sel], dtype=np.int32)   #: Tagging decisions != 0 for selected events
        self.dec_flav   = pd.Series(self.all_B_ID[self.tagged_sel], dtype=np.int32)  #: B meson ids for tagged and selected candidates
        self.dec_flav   //= get_absid(self.dec_flav)
        self.prod_flav  = self.dec_flav.copy(deep=True)                              #: Production flavour estimate
        self.eta        = pd.Series(self.all_eta[self.tagged_sel])                   #: Mistag of tagged and selected candidates
        self.avg_eta    = np.mean(self.eta)                                          #: mean mistag of selected tagged events
        if self.all_tau is not None:
            self.tau = self.all_tau[self.tagged_sel]
        else:
            self.tau = None
        if self.all_tauerr is not None:
            self.tauerr = self.all_tauerr[self.tagged_sel]
        else:
            self.tauerr = None

        # Initialize yields and event weights
        self.N   = len(self.all_eta)      #: Number of events
        self.Ns  = self.selected.sum()    #: Number of selected events
        self.Nt  = self.tagged.sum()      #: Number of tagged events
        self.Nts = self.tagged_sel.sum()  #: Number of selected and tagged events

        if weights is None:
            self.weights = pd.Series(np.ones(self.Nts))  #: Event weight
        else:
            raise_error(len(weights) == self.N, "Tagging data must have matching dimensions")
            self.weights = pd.Series(weights, copy=True)[self.tagged & self.selected].copy(deep=True)
        self.weights.index = self.dec.index

        self.all_weights = pd.Series(weights) if weights is not None else np.ones(self.N)  #: All event weights
        self.Nw          = np.sum(self.all_weights)                  #: Weighted number of all events
        self.Neff        = self.Nw**2 / np.sum(self.all_weights**2)  #: Effective number of all events ((sum w)^2/(sum(w^2)))
        self.Nwt         = np.sum(self.all_weights[self.tagged])     #: Weighted number of all tagged events

        self.Nws         = np.sum(self.all_weights[self.selected])                   #: Weighted number of selected events
        self.Neffs       = self.Nws**2 / np.sum(self.all_weights[self.selected]**2)  #: Effective number selected events
        self.Nwts        = np.sum(self.weights)                                      #: Weighted number of selected and tagged events

        self.correct_tags = self.dec == self.prod_flav  #: Tag corresponds to production flavour (for selected events)
        self.wrong_tags   = ~self.correct_tags          #: Tag does not correspond to production flavour (for selected events)

        raise_error(self.Nt > 0 and self.Nts > 0 and self.Ns > 0, "No events left after cut = invalid tag data")
        self.tau = None
        self.tauerr = None
        self.__validate()

    def _init_timeinfo(self, mode, DM, DG, resolution_model):
        # Initialize tagged decay times
        if mode == "Bd":
            self.tau    = pd.Series(self.all_tau)[self.tagged_sel]  #: decay time in picoseconds
            self.tauerr = pd.Series(self.all_tauerr)[self.tagged_sel] if self.all_tauerr is not None else None  #: decay time uncertainty in picoseconds
        elif mode == "Bs":
            self.tau    = pd.Series(self.all_tau)[self.tagged_sel]
            self.tauerr = pd.Series(self.all_tauerr)[self.tagged_sel] if self.all_tauerr is not None else None
        elif mode == "Bu":
            self.tau    = None
            self.tauerr = None

        # Computes flavour impurity for each event. If oscillation probability
        # is > 50%, production flavour is assumed to be the opposite
        if mode == "Bu":
            self.osc_dilution = np.zeros(self.Nts)
            Amix = None
        else:
            Amix = mixing_asymmetry(self.tau[self.tagged_sel],
                                    DM     = DM,
                                    DG     = DG,
                                    tauerr = self.tauerr,
                                    a      = 0,
                                    res    = resolution_model)
            self.osc_dilution = 0.5 * (1.0 - np.abs(Amix))

        # Update production asymmetry given mixing asymmetry
        # and measures of "tag correctness"
        if mode != "Bu":
            self.prod_flav = self.dec_flav.copy()
            self.prod_flav[np.sign(Amix) == -1] *= -1

            self.correct_tags = self.dec == self.prod_flav
            self.wrong_tags   = ~self.correct_tags

        self.__validate()

    def __validate(self):
        # Check whether data is aligned
        assert len(self.all_eta)    == self.N
        assert len(self.all_dec)    == self.N
        assert len(self.all_B_ID)   == self.N
        assert len(self.selected)   == self.N
        assert len(self.tagged)     == self.N
        assert len(self.tagged_sel) == self.N

        assert len(self.eta)        == self.Nts
        assert len(self.dec)        == self.Nts
        assert len(self.prod_flav)  == self.Nts
        assert len(self.dec_flav)   == self.Nts
        if self.all_tau is not None:
            assert len(self.all_tau) == self.N
        if self.tau is not None:
            assert len(self.tau) == self.Nts
        if self.all_tauerr is not None:
            assert len(self.all_tauerr) == self.N
        if self.tauerr is not None:
            assert len(self.tauerr) == self.Nts

    def __str__(self):
        return ("Tagging Statistics\n"
                f"N  = {self.N}\n"
                f"Nw = {self.Nw}\n"
                f"Nt = {self.Nt}\n"
                f"Nwt = {self.Nwt}\n"
                f"Ns  = {self.Ns}\n"
                f"Nws = {self.Nws}\n"
                f"Nts = {self.Nts}\n"
                f"Nwts = {self.Nwts}")

    def __eq__(self, other):
        """ return true if data of two TaggingData objects is identical.
            Needed for unit testing
        """
        equal = True
        equal &= self.all_eta.equals(other.all_eta)
        equal &= self.all_dec.equals(other.all_dec)
        equal &= self.all_B_ID.equals(other.all_B_ID)
        equal &= self.tagged.equals(other.tagged)
        equal &= self.dec.equals(other.dec)
        equal &= self.dec_flav.equals(other.dec_flav)
        equal &= self.prod_flav.equals(other.prod_flav)
        equal &= self.eta.equals(other.eta)
        equal &= self.avg_eta == other.avg_eta
        equal &= self.weights.equals(other.weights)
        equal &= self.all_weights.equals(other.all_weights)
        equal &= self.correct_tags.equals(other.correct_tags)
        equal &= self.wrong_tags.equals(other.wrong_tags)

        equal &= self.N     == other.N
        equal &= self.Nt    == other.Nt
        equal &= self.Nw    == other.Nw
        equal &= self.Neff  == other.Neff
        equal &= self.Nwt   == other.Nwt
        equal &= self.Ns    == other.Ns
        equal &= self.Nts   == other.Nts
        equal &= self.Nws   == other.Nws
        equal &= self.Neffs == other.Neffs
        equal &= self.Nwts  == other.Nwts
        return equal


class BasicTaggingData:
    r"""
    BasicTaggingData
    Type for keeping track of tagging data and basic event statistics of a tagger without knowledge
    about the true prodcution flavour. Used to descibe a Tagger in a target dataset

    :param eta_data: Uncalibrated mistags
    :type eta_data: list
    :param dec_data: Uncalibrated tagging decisions
    :type dec_data: list
    :param weights: Per-event weights
    :type weights: list
    :param ignore_out_of_range: Whether to ignore mistag values :math:`\eta\notin [0,0.5]` (not recommended)
    :type ignore_out_of_range: bool
    """
    def __init__(self, eta_data, dec_data, weights, ignore_eta_out_of_range=False):
        self.all_eta   = pd.Series(eta_data)  #: All eta values
        self.all_dec   = pd.Series(dec_data)  #: All dec values

        self.overflow  = (self.all_eta > 0.5)  #: Mask of events with :math:`\omega>0.5`
        self.underflow = (self.all_eta < 0)    #: Mask of events with :math:`\omega<0`
        self.noverflow = self.overflow.sum()   #: Number of calibrated mistags > 0.5

        if not ignore_eta_out_of_range:
            self.all_eta[self.overflow] = 0.5
            self.all_eta[self.underflow] = 0
            self.all_dec[self.overflow] = 0

        self.tagged    = self.all_dec != 0    #: Mask of tagged events
        self.dec       = pd.Series(self.all_dec[self.tagged], dtype=np.int32)           #: Tagging decisions != 0
        self.eta       = pd.Series(self.all_eta[self.tagged])  #: Mistag of tagged candidates

        self.N  = len(self.all_eta)  #: Number of events
        self.Nt = self.tagged.sum()  #: Number of tagged events

        # Set weights to 1 if not defined
        if weights is None:
            self.weights = pd.Series(np.ones(self.Nt))
        else:
            raise_error(len(weights) == self.N, "Tagging data must have matching dimensions")
            self.weights = pd.Series(weights)[self.tagged].copy(deep=True)
        self.weights.index = self.dec.index

        self.all_weights = pd.Series(weights) if weights is not None else np.ones(self.N)
        self.Nw          = np.sum(self.all_weights)  #: Weighted number of events
        self.Neff        = self.Nw**2 / np.sum(self.all_weights**2)  #: Effective number of total events
        self.Nwt         = np.sum(self.weights)   #: Weighted number of tagged events
