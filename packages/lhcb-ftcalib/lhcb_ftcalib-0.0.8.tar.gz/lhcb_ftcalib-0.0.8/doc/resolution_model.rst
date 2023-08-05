Decay time resolution
=====================

If the decay time uncertainty is passed to the constructor, the mixing
asymmetry is updated as follows

:math:`A_\mathrm{mix}(t) \mapsto \exp\left(-\frac{1}{2}\Delta m^2\sigma_t^2\right)A_\text{mix}(t)`

For this default case, the resolution model of type GaussianResolution does not
need to be passed to the Tagger constructor.  If :math:`\Delta\Gamma` is not
zero, numerical convolutions of a gaussian resolution model with widths
:math:`\sigma_{t,i}` with the mixing asymmetry is performed

.. autoclass:: resolution_model.ResolutionModel
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: resolution_model.GaussianResolution
   :members:
   :undoc-members:
   :show-inheritance:
