# Donor-adjusted forecasting after structural shocks with postshock

## RELAI

- **Examine** the named object `cop_oil_postshock`.
- **eXplain** why the pre-shock baseline is the wrong number.
- **Probe** whether donor weighting is stable or just a cosmetic fix.
- **Link to economics** through post-shock forecasting and synthetic control.
- **Output prediction** before running `python tutorial.py`.
- **Recreate** the summary with `python tutorial.py`.
- **Extend** the same logic to the variance example `iyg_onestep_input`.

## Named object

The named empirical object is `cop_oil_postshock` from the `postshock` vignette. It packages a ConocoPhillips price shock in March 2020 together with five historical donor episodes: the 2008 financial crisis shocks, a 2014 oil shock, and associated pre-shock covariates. The package also ships a second object, `iyg_onestep_input`, for a one-step volatility example around the 2016 U.S. election.

That naming matters. Economists do not need “post-shock forecasting in general”; they need one target episode, a well-defined donor set, and a reproducible alignment between the two.

## Stake

The stake is a forecast made after a large structural break. If you are pricing risk, stress-testing a trading book, or tracking a policy-sensitive series, the pre-shock model can be badly wrong because it extrapolates a regime that has already ended. The number is not a cosmetic detail: it can decide whether a shock response looks manageable or severe.

In the ConocoPhillips example, the unadjusted baseline forecast is 44.734 while the observed post-shock value is 34.070. That is not a rounding issue. It is the kind of wrong number that changes interpretation.

## Naive path

The obvious move is to fit the target series using only its pre-shock history and then forecast forward as if nothing structural changed. In the vignette, that naive path gives 44.734 for the first post-shock observation.

The wrong number is 44.734.

Against the realized 34.070, the absolute error is 10.664. The baseline is informative only in the weakest sense: it tells you the model has carried the old regime into a new one.

This is the point of the tutorial: the failure is visible in the number, not just in the prose.

## Technique

`postshock` fixes the failure by borrowing information from historical donor episodes that experienced comparable shocks. The method is not “throw more data at it.” It is:

- choose donor episodes with economic similarity,
- estimate donor balancing weights from pre-shock covariates,
- estimate donor-specific post-shock effects,
- combine those effects using the weights, and
- add the weighted shock adjustment to the target-series baseline forecast.

The vignette’s ConocoPhillips example shows the logic clearly:

- unadjusted forecast: 44.734
- arithmetic-mean adjustment: 39.750
- DBW-adjusted forecast: 39.110
- observed value: 34.070

The donor-weighted adjustment does not magically make the forecast perfect. It makes the number less wrong. That is the right standard for applied work.

The package also supports structured donor pools. In the vignette, the 2014 oil shock is separated from the 2008 crisis episodes, which is a more honest economic story than collapsing all donors into one blob. That is the extension economists should notice: substantive grouping first, mechanical aggregation second.

`tutorial.py` fetches the public vignette, extracts the reported forecast table, and prints the naive error and the donor-adjusted alternatives. The script is intentionally small so the reader can inspect every line.

## You will get this wrong

The first-week mistakes are predictable:

- **Misaligning the shock date**: the last pre-shock observation is not the first post-shock observation.
- **Using post-shock target information in donor weighting**: that is leakage, not sophistication.
- **Treating donor weights as probabilities**: they are balancing weights, not event frequencies.
- **Confusing matching covariates with model regressors**: `dbw_indices` and `covariate_indices` do different jobs.
- **Assuming one donor pool fits all mechanisms**: an oil supply shock and a crisis shock are not the same object.
- **Believing a smaller error proves identification**: it only says the adjustment helped on this episode.

If you do not check the alignment, you can get a smooth-looking forecast and still be wrong in the economically relevant sense.

## Controversy

This sits on a familiar fault line. One camp reads donor-adjusted forecasting as a pragmatic synthetic-control-style device for shocks and breaks: useful, transparent, and often better than a blind time-series extrapolation. Another camp worries that donor pools, weight regularization, and post-hoc grouping can become tuning knobs that make the forecast look better without changing the economic identification story.

There is also a practical dispute about evaluation. Should we judge these methods by point accuracy on one-step examples, by stability across episodes, or by whether they survive a genuinely out-of-sample shock? The answer changes how much you trust the technique.

That is why the `postshock` vignette is worth reading: it makes the wrong number visible, but it also makes the identification and forecasting trade-offs impossible to ignore.
