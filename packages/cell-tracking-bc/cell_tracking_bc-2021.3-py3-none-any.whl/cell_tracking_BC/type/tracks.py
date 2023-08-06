# Copyright CNRS/Inria/UCA
# Contributor(s): Eric Debreuve (since 2021)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

from __future__ import annotations

import warnings as wrng
from typing import Optional, Sequence

import networkx as grph
from cell_tracking_BC.type.cell import cell_t


class tracks_t(grph.DiGraph):
    def AddTrackSegment(
        self, src_cell: cell_t, tgt_cell: cell_t, src_time_point: int
    ) -> None:
        """"""
        self.add_node(src_cell, time_point=src_time_point)
        self.add_node(tgt_cell, time_point=src_time_point + 1)
        self.add_edge(src_cell, tgt_cell)

    def CleanTracks(self) -> None:
        """"""
        for cell in self.RootCells():
            if cell["time_point"] > 0:
                unordered_tracks = self._UnorderedTracksContainingCell(cell)
                self.remove_nodes_from(unordered_tracks)
            elif self.out_degree(cell) == 0:
                self.remove_node(cell)

    def IsConform(self, when_fails: str = "warn silently") -> bool:
        """
        when_fails:
            - "warn silently": Return a boolean
            - "warn aloud": Print a message and return a boolean
            - "raise": Raises a ValueError exception
        """
        issues = []

        for cell in self.nodes:
            if (n_predecessors := self.in_degree(cell)) > 1:
                issues.append(f"{cell}: {n_predecessors} predecessors; Expected=0 or 1")
            elif (n_successors := self.out_degree(cell)) > 2:
                issues.append(
                    f"{cell}: {n_successors} successors; Expected=0 or 1 or 2"
                )

        for cell in self.RootCells():
            if cell["time_point"] > 0:
                issues.append(
                    f"{cell}: Root cell with non-zero time point ({cell['time_point']})"
                )
            if self.out_degree(cell) == 0:
                issues.append(f"{cell}: Empty track")

        if issues.__len__() > 0:
            if when_fails == "warn silently":
                return False
            elif when_fails == "warn aloud":
                issues.append(f"{self}: Conformity Check:")
                wrng.warn("\n".join(issues))
                return False
            elif when_fails == "raise":
                issues.append(f"{self}")
                raise ValueError("\n".join(issues))
            else:
                raise ValueError(f'{when_fails}: Invalid "when_fails" argument value')
        else:
            return True

    def RootCells(self) -> Sequence[cell_t]:
        """"""
        return tuple((_nde for _nde in self.nodes if self.in_degree(_nde) == 0))

    def DividingCells(self) -> Sequence[cell_t]:
        """"""
        return tuple((_nde for _nde in self.nodes if self.out_degree(_nde) == 2))

    def LeafCells(self) -> Sequence[cell_t]:
        """"""
        return tuple((_nde for _nde in self.nodes if self.out_degree(_nde) == 0))

    def TracksFromRoot(self, root: cell_t) -> Sequence[grph.DiGraph]:
        """"""
        unordered = self._UnorderedTracksContainingCell(root)
        if unordered is None:
            return ()

        output = []

        leaves = (_nde for _nde in unordered.nodes if unordered.out_degree(_nde) == 0)
        for leaf in leaves:
            track = grph.shortest_path(unordered, source=root, target=leaf)
            output.append(track)

        return output

    def TrackToLeaf(self, leaf: cell_t) -> Optional[grph.DiGraph]:
        """"""
        unordered = self._UnorderedTracksContainingCell(leaf)
        if unordered is None:
            return None

        root = (_nde for _nde in unordered.nodes if unordered.in_degree(_nde) == 0)

        return grph.shortest_path(unordered, source=root, target=leaf)

    def _UnorderedTracksContainingCell(self, cell: cell_t) -> Optional[grph.DiGraph]:
        """"""
        for component in grph.weakly_connected_components(self):
            if cell in component:
                return self.subgraph(component)

        return None

    def __str__(self) -> str:
        """"""
        return (
            f"{self.__class__.__name__.upper()}.{id(self)}\n"
            f"{self.nodes.__len__()=}\n"
            f"{self.edges.__len__()=}"
        )
