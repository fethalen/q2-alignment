# ----------------------------------------------------------------------------
# Copyright (c) 2025, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
from q2_types.feature_data import (
    AlignedDNASequencesDirectoryFormat,
    AlignedProteinSequencesDirectoryFormat,
    DNAFASTAFormat,
    FASTAFormat,
    ProteinFASTAFormat,
)
from q2_types.genome_data import GenesDirectoryFormat, ProteinsDirectoryFormat
from qiime2.util import duplicate
from qiime2 import Artifact

from q2_alignment.plugin_setup import plugin


@plugin.register_transformer
def _1(seqs: FASTAFormat) -> AlignedProteinSequencesDirectoryFormat:
    aligned_dir_fmt = AlignedProteinSequencesDirectoryFormat()
    duplicate(
        src=seqs.path,
        dst=aligned_dir_fmt.path / aligned_dir_fmt.file.pathspec
    )
    return aligned_dir_fmt


@plugin.register_transformer
def _2(seqs: FASTAFormat) -> AlignedDNASequencesDirectoryFormat:
    aligned_dir_fmt = AlignedDNASequencesDirectoryFormat()
    duplicate(
        src=seqs.path,
        dst=aligned_dir_fmt.path / aligned_dir_fmt.file.pathspec
    )
    return aligned_dir_fmt


@plugin.register_transformer
def _3(seq_set: GenesDirectoryFormat) -> DNAFASTAFormat:
    fasta_dir_fmt = DNAFASTAFormat()
    duplicate(
        src=seq_set.path,
        dst=fasta_dir_fmt.path / fasta_dir_fmt.file.pathspec
    )
    return fasta_dir_fmt


@plugin.register_transformer
def _4(seq_set: ProteinsDirectoryFormat) -> ProteinFASTAFormat:
    # fasta_dir_fmt = ProteinFASTAFormat()

    files = list(seq_set.proteins.iter_views(ProteinFASTAFormat))

    if len(files) != 1:
        raise ValueError(
            "Expected exactly one FASTA file in ProteinsDirectoryFormat "
            f"but found {len(files)}."
        )

    # src = files[0]

    return files[0][1]

    # seq_set.write(str(fasta_dir_fmt.path))
    # return Artifact.import_data("SingleDNASequence", fasta_dir_fmt)
