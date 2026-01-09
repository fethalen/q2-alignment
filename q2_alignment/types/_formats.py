# ----------------------------------------------------------------------------
# Copyright (c) 2025, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ---------------------------------------------------------------------------
import qiime2.plugin.model as model
from q2_types._util import FileDictMixin

from q2_types.feature_data import (
    AlignedDNAFASTAFormat,
    AlignedProteinFASTAFormat,
)


class AlignedGenesDirectoryFormat(model.DirectoryFormat, FileDictMixin):
    pathspec = r'.+\.(fa|fna|fasta)$'
    genes = model.FileCollection(pathspec, format=AlignedDNAFASTAFormat)

    @genes.set_path_maker
    def genes_path_maker(self, genome_id):
        return '%s.fasta' % genome_id


class AlignedProteinsDirectoryFormat(model.DirectoryFormat, FileDictMixin):
    pathspec = r'.+\.(fa|faa|fasta)$'
    proteins = model.FileCollection(pathspec, format=AlignedProteinFASTAFormat)

    @proteins.set_path_maker
    def proteins_path_maker(self, genome_id):
        return '%s.fasta' % genome_id
