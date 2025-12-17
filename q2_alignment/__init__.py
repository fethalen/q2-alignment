# ----------------------------------------------------------------------------
# Copyright (c) 2016-2025, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from ._mafft import (
    _mafft,
    mafft,
    mafft_add,
    SequenceType,
    align_orthogroups,
)
from ._filter import mask

from .partition import (
    partition_orthogroup_sequences,
    collate_orthogroup_msas,
)

from q2_alignment.types import (
    Orthogroups,
    DNASequences,
    ProteinSequences,
    AlignedGenes,
    AlignedProteins,
    AlignedDNASequences,
    AlignedProteinSequences,
    AlignedGenesDirectoryFormat,
    AlignedProteinsDirectoryFormat,
)

try:
    from ._version import __version__
except ModuleNotFoundError:
    __version__ = '0.0.0+notfound'

__all__ = [
    '_mafft',
    'mafft',
    'mask',
    'mafft_add',
    'SequenceType',
    'DNASequences',
    'ProteinSequences',
    'Orthogroups',
    'partition_orthogroup_sequences',
    'collate_orthogroup_msas',
    'align_orthogroups',
    'AlignedGenes',
    'AlignedProteins',
    'AlignedDNASequences',
    'AlignedProteinSequences',
    'AlignedGenesDirectoryFormat',
    'AlignedProteinsDirectoryFormat',
]
