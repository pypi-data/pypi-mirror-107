"""
OP2 parser based on Steve Doyle OP2
https://pynastran-git.readthedocs.io/en/latest/quick_start/op2_demo_numpy1.html
"""


import logging
import os
from collections import namedtuple

import numpy as np
import pandas as pd
from pyNastran.op2.op2 import read_op2
from pyNastran.utils import object_attributes, object_methods

from mystran_validation.parsers import subset

Resmap = namedtuple(
    "Result",
    ["attr", "columns", "discard", "index"],
    defaults=[None, None, ["SubcaseID"]],
)


# -----------------------------------------------------------------------------
# misc config for common results
RESMAP = {
    "displacements": Resmap(
        attr="displacements",
        # columns=["SubcaseID", "NodeID", "Type", "1", "2", "3", "4", "5", "6"],
        discard=["Type"],
        index=["SubcaseID", "NodeID"],
    ),
    "loads": Resmap(
        attr="load_vectors",
        columns=["SubcaseID", "NodeID", "Type", "1", "2", "3", "4", "5", "6"],
        discard=["Type"],
        index=["SubcaseID", "NodeID"],
    ),
    "reactions": Resmap(
        attr="spc_forces",
        # columns=["SubcaseID", "NodeID", "Type", "1", "2", "3", "4", "5", "6"],
        discard=["Type"],
        index=["SubcaseID", "NodeID"],
    ),
    "gpf": Resmap(
        attr="grid_point_forces",
        # 	SubcaseID 		NodeID 	ElementID 	ElementType 	f1 	f2 	f3 	m1 	m2 	m3
        columns=[
            "SubcaseID",
            "NodeID",
            "eid",
            "etype",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
        ],
        index=["SubcaseID", "eid", "NodeID"],
    ),
    "cbar_force": Resmap(
        attr="cbar_force",
        index=["SubcaseID", "ElementID"],
    ),
    "cbush_force": Resmap(
        attr="cbush_force",
        index=["SubcaseID", "ElementID"],
    ),
}


class Parser:
    """ """

    def __init__(self, fpath, mode="nx"):
        self.op2 = read_op2(fpath, build_dataframe=False, debug=False, mode=mode)

    def _process(self, attribute, raw=False, **levels):
        lcids = {}
        predef = RESMAP.get(attribute)
        if predef:
            attrname = predef.attr
        else:
            attrname = attribute
        attr = getattr(self.op2, attrname)
        for lcid, data in attr.items():
            data.build_dataframe()
            lcids[lcid] = data.data_frame
        df = pd.concat(lcids)
        # level one sometime sis row number
        # sometimes NodeID...
        df.reset_index(level=1, inplace=True)

        df.index.names = ["SubcaseID"]
        df.reset_index(inplace=True)

        if predef and not raw:
            if predef.columns:
                df.columns = predef.columns
            if predef.discard:
                cols = list(predef.discard) + [
                    c for c in df.columns if c.startswith("level_")
                ]
                df = df.drop(columns=cols)
            if predef.index:
                df = df.set_index(predef.index)
        return subset(df, **levels)

    def get_displacements(self, raw=False, **levels):
        return self._process("displacements", raw=raw, **levels)

    def get_reactions(self, raw=False, **levels):
        df = self._process("reactions", raw=raw, **levels)
        # drop rows where everithing is 0
        # df = df[df.abs() > 0].dropna(how="all").fillna(0)
        return df

    def get_loads(self, raw=False, **levels):
        df = self._process("loads", raw=raw, **levels)
        # drop rows where everithing is 0
        df = df[df.abs() > 0].dropna(how="all").fillna(0)
        return df

    def get_cbar_force(self, raw=False, **levels):
        df = self._process("cbar_force", raw=raw, **levels)
        return df

    def get_cbush_force(self, raw=False, **levels):
        df = self._process("cbush_force", raw=raw, **levels)
        return df

    def get_forces(self, axis, raw=False, **levels):
        """extract element forces. This is trickier than others since we need to interrogate
        several tables depending on axis request.

        * In global axis request, we will interrogate gridpoint forces
        * In local axis, we will interrogate bar and bush forces
        """
        if axis == "global":
            return self.get_global_forces(raw=raw, **levels)
        else:
            df_bars = self._process("cbar_force")
            breakpoint()
            df_bars.columns = pd.MultiIndex.from_tuples(
                [c.split("_") for c in df_bars.columns]
            )
            df_bars_A = df_bars
            df_bushes_A = self._process("cbush_force")
            df_bushes_B = -df_bushes_A
            raise NotImplementedError(
                f"OP2 recovering of forces in {axis} axis is not implemented"
            )
        pass

    def get_gpf(self, **levels):
        df = self._process("gpf")
        df.etype = df.etype.str.strip()
        df.set_index("etype", append=True, inplace=True)
        return subset(df, **levels).sort_index()

    def get_global_forces(self, **levels):
        """recover grid point forces filtered by elements BAR & BUSH"""
        df = self.get_gpf(etype=["BAR", "BUSH"])
        df.reset_index(level=-1, drop=True, inplace=True)  # drop etype
        return subset(df, **levels) * -1
