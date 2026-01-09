# ----------------------------------------------------------------------------
# Copyright (c) 2016-2025, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
from qiime2.plugin import SemanticType

from q2_types.genome_data import GenomeData

Orthogroups = SemanticType('Orthogroups',
                           field_names='type')
DNASequences = SemanticType('DNASequences',
                            variant_of=Orthogroups.field['type'])
AlignedDNASequences = SemanticType('AlignedDNASequences',
                                   variant_of=Orthogroups.field['type'])
ProteinSequences = SemanticType('ProteinSequences',
                                variant_of=Orthogroups.field['type'])
AlignedProteinSequences = SemanticType('AlignedProteinSequences',
                                       variant_of=Orthogroups.field['type'])
AlignedGenes = SemanticType('AlignedGenes',
                            variant_of=GenomeData.field['type'])
AlignedProteins = SemanticType('AlignedProteins',
                               variant_of=GenomeData.field['type'])
