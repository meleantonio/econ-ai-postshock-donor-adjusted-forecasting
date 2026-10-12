from __future__ import annotations

import json
from dataclasses import dataclass

import pandas as pd
import requests

URL = "https://cran.r-project.org/web/packages/postshock/vignettes/postshock-workflow.html"


@dataclass
class ForecastSummary:
    observed: float
    unadjusted: float
    arithmetic_mean: float
    adjusted: float

    @property
    def naive_error(self) -> float:
        return abs(self.unadjusted - self.observed)

    @property
    def adjusted_error(self) -> float:
        return abs(self.adjusted - self.observed)



def _find_table_with_rows(tables: list[pd.DataFrame], required_rows: list[str]) -> pd.DataFrame:
    for table in tables:
        text = " ".join(table.astype(str).fillna("").to_numpy().ravel())
        if all(row.lower() in text.lower() for row in required_rows):
            return table
    raise RuntimeError(f"Could not find a table containing rows: {required_rows}")



def extract_conoco_phillips_summary(html: str) -> ForecastSummary:
    tables = pd.read_html(html)
    cop = _find_table_with_rows(tables, ["Observed value", "Unadjusted", "DBW adjusted"])

    methods = cop.iloc[:, 0].astype(str).str.strip().tolist()
    values = cop.iloc[:, 1].astype(float).tolist()
    mapping = dict(zip(methods, values))
    return ForecastSummary(
        observed=mapping["Observed value"],
        unadjusted=mapping["Unadjusted"],
        arithmetic_mean=mapping["Arithmetic mean"],
        adjusted=mapping["DBW adjusted"],
    )



def extract_iyg_proxy(html: str) -> dict[str, float]:
    tables = pd.read_html(html)
    iyg = _find_table_with_rows(tables, ["Observed squared-return proxy", "Unadjusted", "DBW adjusted"])
    methods = iyg.iloc[:, 0].astype(str).str.strip().tolist()
    values = iyg.iloc[:, 1].astype(float).tolist()
    return dict(zip(methods, values))



def main() -> None:
    resp = requests.get(URL, timeout=30)
    resp.raise_for_status()
    html = resp.text

    cop = extract_conoco_phillips_summary(html)
    iyg = extract_iyg_proxy(html)

    report = {
        "primary_source": URL,
        "cop_oil_postshock": {
            "observed": cop.observed,
            "unadjusted": cop.unadjusted,
            "arithmetic_mean": cop.arithmetic_mean,
            "adjusted": cop.adjusted,
            "naive_wrong_number": cop.unadjusted,
            "naive_absolute_error": round(cop.naive_error, 3),
            "adjusted_absolute_error": round(cop.adjusted_error, 3),
        },
        "iyg_onestep_input_proxy": {
            "observed_squared_return_proxy": iyg["Observed squared-return proxy"],
            "unadjusted": iyg["Unadjusted"],
            "adjusted": iyg["DBW adjusted"],
        },
    }

    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
