# ----------------------------------------------------------------------------
# Copyright (c) 2025, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ---------------------------------------------------------------------------
import glob
import os
import warnings

import numpy as np

from typing import Union, List
from qiime2.util import duplicate

from ._mafft import SequenceType

from .types import (
    Orthogroups,
    DNASequences,
    ProteinSequences,
)

from q2_types.genome_data import (
    GenesDirectoryFormat,
    ProteinsDirectoryFormat
)


def partition_orthogroup_dna_sequences(
    sequence_sets: GenesDirectoryFormat,
    num_partitions: int | None = None,
) -> GenesDirectoryFormat:
    return partition_orthogroup_sequences(sequence_sets, num_partitions)


def partition_orthogroup_protein_sequences(
    sequence_sets: ProteinsDirectoryFormat,
    num_partitions: int | None = None,
) -> ProteinsDirectoryFormat:
    return partition_orthogroup_sequences(sequence_sets, num_partitions)


def partition_orthogroup_sequences(
    sequence_sets: Union[GenesDirectoryFormat, ProteinsDirectoryFormat],
    num_partitions: int | None = None,
) -> Union[GenesDirectoryFormat, ProteinsDirectoryFormat]:
    if isinstance(sequence_sets, GenesDirectoryFormat):
        sequence_type = SequenceType.NUCLEOTIDE
    elif isinstance(sequence_sets, ProteinsDirectoryFormat):
        sequence_type = SequenceType.PROTEIN

    partitioned_sequence_sets = {}

    all_files = glob.glob(os.path.join(str(sequence_sets), "*"))

    sequence_sets = [
        f for f in all_files
        if f.endswith((".fa", ".faa", ".fasta"))
    ]
    names = [
        os.path.splitext(os.path.basename(f))[0]
        for f in sequence_sets
    ]

    sequence_sets = list(zip(names, sequence_sets))
    num_sequence_sets = len(sequence_sets)

    if num_partitions is None:
        num_partitions = num_sequence_sets
    elif num_partitions < num_sequence_sets:
        warnings.warn(
            "You have requested a number of partitions"
            f" '{num_partitions}' that is greater than your number"
            f" of sequence sets: '{num_sequence_sets}.' Your data will be"
            f" partitioned by sample into '{num_sequence_sets}'"
            " partitions."
        )
        num_partitions = num_sequence_sets

    sequence_sets = np.array_split(sequence_sets, num_partitions)

    for i, sequence_set in enumerate(sequence_sets, 1):
        if sequence_type.is_nucleotide():
            result = GenesDirectoryFormat()
        elif sequence_type.is_protein():
            result = ProteinsDirectoryFormat()

        for sequence_set_name, sequence_set_fp in sequence_set:
            duplicate(
                sequence_set_fp,
                result.path / os.path.basename(sequence_set_fp)
            )

        if num_partitions == num_sequence_sets:
            partitioned_sequence_sets[sequence_set_name] = result
        else:
            partitioned_sequence_sets[i] = result

    return partitioned_sequence_sets


def collate_orthogroup_msas(
    alignment_sets: Union[GenesDirectoryFormat, ProteinsDirectoryFormat],
) -> Union[GenesDirectoryFormat, ProteinsDirectoryFormat]:
    if isinstance(alignment_sets[0], GenesDirectoryFormat):
        collated_alignments = GenesDirectoryFormat()
    elif isinstance(alignment_sets[0], ProteinsDirectoryFormat):
        collated_alignments = ProteinsDirectoryFormat()

    for alignment in alignment_sets:
        for fp in alignment.path.iterdir():
            duplicate(fp, collated_alignments.path / fp.name)

    return collated_alignments
