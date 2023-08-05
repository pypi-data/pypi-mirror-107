import numpy as np
import pandas as pd

from lhcb_ftcalib.plotting import draw_calibration_curve
from lhcb_ftcalib.combination import combine_taggers
from lhcb_ftcalib.printing import (print_tagger_correlation, print_tagger_performances, print_tagger_statistics,
                                   print_calibration_info, epmstyle_header, section_header, printbold, raise_warning,
                                   raise_error)
from lhcb_ftcalib.Tagger import Tagger


class TaggerCollection:
    r""" class TaggerCollection
        Lists type for grouping taggers. Supports iteration.

        :param \*taggers: Tagger instance
        :type \*taggers: Tagger
    """
    def __init__(self, *taggers):
        self._taggers = [*taggers]
        self._index = -1
        if self._taggers:
            self._validate()

    def __str__(self):
        return "TaggerCollection [" + ','.join([t.name for t in self._taggers]) + "]"

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        return len(self._taggers)

    def __iter__(self):
        return self

    def __next__(self):
        if self._index == len(self._taggers) - 1:
            self._index = -1
            raise StopIteration
        self._index += 1
        return self._taggers[self._index]

    def __getitem__(self, t):
        return self._taggers[t]

    def _validate(self):
        assert all([isinstance(tagger, Tagger) for tagger in self]), "TaggerCollection can only store Tagger instances"
        assert len(set([tagger.name for tagger in self])) == len(self._taggers), "Tagger names are not unique"
        assert len(set([tagger.stats.N for tagger in self])) == 1, "Data of Taggers have inconsistent lenghts"

    def set_calibration(self, func):
        """ Sets this calibration function for all taggers

            :param func: Calibration function
            :type func: CalibrationFunction
        """
        for tagger in self:
            tagger.set_calibration(func)

    def add_taggers(self, *tagger):
        """ Adds tagger(s) to the TagCollection instance """
        self._taggers += [*tagger]
        self._validate()

    def create_tagger(self, *args, **kwargs):
        """ Adds a tagger to the TaggerCollection instance
            by passing the arguments to the Tagger() constructor.
        """
        self._taggers.append(Tagger(*args, **kwargs))
        self._validate()

    def calibrate(self, quiet=False, ignore_eta_out_of_range=False):
        """ Loops over taggers, calibrates taggers and prints tagging information
            both before and after the calibrations.

            :param quiet: Whether to print performance summary tables
            :type quiet: bool
            :param ignore_eta_out_of_range: Whether to ignore out of range values of the calibrated mistag (NOT recommended)
            :type ignore_eta_out_of_range: bool
        """
        # Sanity checks
        raise_warning(len(set([t.name for t in self])) == len(self._taggers), "ERROR: Tagger names not unique")

        if not quiet:
            print_tagger_correlation(self, "all")
            print_tagger_performances(self, calibrated=False)
            print_tagger_statistics(self, calibrated=False)

        epmstyle_header("Running calibrations")
        for tagger in self:
            tagger.calibrate(ignore_eta_out_of_range)

        for tagger in self:
            print_calibration_info(tagger)

        if not quiet:
            print_tagger_statistics(self, calibrated=True)
            print_tagger_performances(self, calibrated=True)

    def get_dataframe(self, calibrated=True):
        """ Returns a dataframe of the calibrated mistags and tagging decisions

            :return: Calibrated data
            :return type: pandas.DataFrame
        """
        df = pd.DataFrame()
        if calibrated:
            for tagger in self:
                assert tagger.is_calibrated()
                df[tagger.name + "_CDEC"]  = np.array(tagger.cstats.all_dec.copy(), dtype=np.int32)
                df[tagger.name + "_OMEGA"] = tagger.cstats.all_eta.copy()
        else:  # Only makes sense if user writes an uncalibrated combination to file
            for tagger in self:
                df[tagger.name + "_DEC"] = np.array(tagger.stats.all_dec.copy(), dtype=np.int32)
                df[tagger.name + "_ETA"] = tagger.stats.all_eta.copy()

        return df

    def plot_calibration_curves(self, **kwargs):
        r""" Plots calibration curves of a set of taggers, like the EPM does after the calibrations.

            :param \**kwargs: Arguments to pass to draw_calibration_curve
        """
        section_header("Plotting")
        for tagger in self:
            print("Info: pdf file", draw_calibration_curve(tagger, **kwargs), "has been created")

    def combine_taggers(self, name, calibrated, next_selection=None):
        """ Computes the combination of multiple taggers
            and returns it in the form of a new Tagger object

            :param name: Name of the tagger combination
            :type name: str
            :param calibrated: Whether to use calibrated tagger data for combination (recommended)
            :type calibrated: bool
            :param next_selection: Event selection to use for calibrating combination (default: No selection)
            :type next_selection: list
            :return: Tagger combination
            :rtype: Tagger
        """
        taggernames = [t.name for t in self]
        section_header("TAGGER COMBINATION")
        printbold("Combining taggers " + " ".join(taggernames) + f" into {name}")
        printbold("Checking compatibility")

        # Sanity checks
        for tagger in self:
            raise_error(tagger.stats.all_B_ID.equals(self._taggers[0].stats.all_B_ID), "Taggers must refer to the same pp collision, otherwise combination is nonsense")
        raise_warning(name not in taggernames, "Name of combination is already in use")
        if calibrated:
            indeed_calibrated = [t.cstats is not None for t in self]  # Do not forbid combination of calibrated and uncalibrated taggers
            raise_warning(all(indeed_calibrated), "None, or not all provided taggers have been calibrated")

        printbold("Running combination...")
        # Collect data
        if calibrated:
            decs   = np.array([ np.array(tagger.cstats.all_dec if cal else tagger.stats.all_dec) for tagger, cal in zip(self._taggers, indeed_calibrated) ]).T
            omegas = np.array([ np.array(tagger.cstats.all_eta if cal else tagger.stats.all_eta) for tagger, cal in zip(self._taggers, indeed_calibrated) ]).T
        else:
            decs   = np.array([ np.array(tagger.stats.all_dec) for tagger in self ]).T
            omegas = np.array([ np.array(tagger.stats.all_eta) for tagger in self ]).T

        d_combined, omega_combined = combine_taggers(decs, omegas)

        # Construct Tagger object
        combination = Tagger(name      = name,
                             eta_data  = omega_combined,
                             dec_data  = d_combined,
                             B_ID      = self._taggers[0].stats.all_B_ID,
                             mode      = self._taggers[0].mode,
                             tau_ps    = self._taggers[0].stats.all_tau,
                             tauerr_ps = self._taggers[0].stats.all_tauerr,
                             weight    = self._taggers[0].stats.all_weights,
                             selection = next_selection)
        printbold(f"New tagger combination {combination.name} has been created")
        return combination
