# ----------------------------------------------------------------------------
# Copyright (c) 2016-2025, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from q2_types.feature_data import (
    FeatureData,
    Sequence,
    AlignedSequence,
    ProteinSequence,
    AlignedProteinSequence,
)
from q2_types.genome_data import (
    GenesDirectoryFormat,
    ProteinsDirectoryFormat,
)
from qiime2.plugin import (
    Bool,
    Citations,
    Float,
    Plugin,
    Range,
    Threads,
    TypeMap,
    TypeMatch
)
from qiime2.plugin import (
    Int,
    Collection,
)
from q2_alignment import (
    AlignedGenes,
    AlignedProteins,
    SequenceType,
    DNASequences,
    AlignedDNASequences,
    ProteinSequences,
    AlignedProteinSequences,
    Orthogroups,
)
import importlib
import q2_alignment

T_GenericSequenceInput, T_GenericAlignedSequenceOutput = TypeMap({
    FeatureData[Sequence]:
        FeatureData[AlignedSequence],
    FeatureData[ProteinSequence]:
        FeatureData[AlignedProteinSequence],
})

T_MatchAlignedSequenceType = TypeMatch([
    FeatureData[AlignedSequence],
    FeatureData[AlignedProteinSequence],
])

T_GenericSequenceSetsInput, T_GenericAlignedSequenceSetsOutput = TypeMap({
    Orthogroups[DNASequences]:
        Orthogroups[AlignedDNASequences],
    Orthogroups[ProteinSequences]:
        Orthogroups[AlignedProteinSequences],
})

T_GenericSequenceSetsInput, T_GenericAlignedSequenceSetsOutput = TypeMap({
    Orthogroups[DNASequences]:
        Orthogroups[AlignedDNASequences],
    Orthogroups[ProteinSequences]:
        Orthogroups[AlignedProteinSequences],
})

T_MatchAlignedSequenceSets = TypeMatch([
    Orthogroups[AlignedDNASequences],
    Orthogroups[AlignedProteinSequences],
])

partition_params = {"num_partitions": Int % Range(1, None)}
partition_param_descriptions = {
    "num_partitions": (
        "The number of partitions to split the sequence sets"
        "into."
    )
}

mafft_params = {
    "n_threads": Threads,
    "parttree": Bool,
    "large": Bool
}
mafft_param_descriptions = {
    "n_threads": "The number of threads. (Use `auto` to automatically use "
                 "all available cores)",
    "parttree": "This flag is required if the number of sequences being "
                "aligned are larger than 1,000,000. Disabled by default.",
    "large": "This flag is required when aligning very large datasets "
             "that do not otherwise fit into memory. Temporary data is "
             "then stored in files, instead of RAM. The --use-cache "
             "flag specifies the storage location of the temporary files "
             "created. By default, $TMP/qiime2/ is used.",
}

citations = Citations.load('citations.bib', package='q2_alignment')
plugin = Plugin(
    name='alignment',
    version=q2_alignment.__version__,
    website='https://github.com/qiime2/q2-alignment',
    package='q2_alignment',
    description=('This QIIME 2 plugin provides support for generating '
                 'and manipulating sequence alignments.'),
    short_description='Plugin for generating and manipulating alignments.'
)

plugin.methods.register_function(
    function=q2_alignment.partition.partition_orthogroup_dna_sequences,
    inputs={"sequence_sets": Orthogroups[DNASequences]},
    parameters={**partition_params},
    outputs={"partitioned_sequence_sets":
             Collection[Orthogroups[DNASequences]]},
    name="Collates multiple alignment directories into one.",
    description="Collates multiple alignment directories into one.",
    parameter_descriptions={
        **partition_param_descriptions,
    },
    output_descriptions={
        'partitioned_sequence_sets': 'A set of MSAs divided into partitions.'
    },
)

plugin.methods.register_function(
    function=q2_alignment.partition.partition_orthogroup_protein_sequences,
    inputs={"sequence_sets": Orthogroups[ProteinSequences]},
    parameters={**partition_params},
    outputs={"partitioned_sequence_sets":
             Collection[Orthogroups[ProteinSequences]]},
    name="Collates multiple alignment directories into one.",
    description="Collates multiple alignment directories into one.",
    parameter_descriptions={
        **partition_param_descriptions,
    },
    output_descriptions={
        'partitioned_sequence_sets': 'A set of MSAs divided into partitions.'
    },
)

plugin.methods.register_function(
    function=q2_alignment.partition.collate_orthogroup_msas,
    inputs={"alignment_sets": Collection[T_MatchAlignedSequenceSets]},
    parameters={},
    outputs={"collated_alignments": T_MatchAlignedSequenceSets},
    name="Collates multiple alignment directories into one.",
    description="Collates multiple alignment directories into one.",
    input_descriptions={
        'alignment_sets': 'Set(s) of multiple sequence alignments (MSAs).'
    },
    output_descriptions={
        'collated_alignments': 'A collated set of MSAs.'
    },
)

plugin.pipelines.register_function(
    function=q2_alignment.align_orthogroups,
    inputs={'sequence_sets': T_GenericSequenceSetsInput},
    parameters={
        **mafft_params,
        **partition_params
    },
    outputs=[('alignment', T_GenericAlignedSequenceSetsOutput)],
    input_descriptions={
        'sequence_sets': 'The set of orthogroup sequences to be aligned.'
    },
    parameter_descriptions={
        **mafft_param_descriptions,
        **partition_param_descriptions
    },
    output_descriptions={'alignment': 'The aligned sequences.'},
    name='Perform de novo multiple sequence alignment using MAFFT on a set of '
         'orthogroup sequences.',
    description='Perform de novo multiple sequence alignment using MAFFT on a '
                'set of orthogroup sequences.',
    citations=[citations['katoh2013mafft']]
)

plugin.methods.register_function(
    function=q2_alignment.mafft,
    inputs={'sequences': T_GenericSequenceInput},
    parameters={**mafft_params},
    outputs=[('alignment', T_GenericAlignedSequenceOutput)],
    input_descriptions={'sequences': 'The sequences to be aligned.'},
    parameter_descriptions={**mafft_param_descriptions},
    output_descriptions={'alignment': 'The aligned sequences.'},
    name='De novo multiple sequence alignment with MAFFT',
    description=("Perform de novo multiple sequence alignment using MAFFT."),
    citations=[citations['katoh2013mafft']]
)

plugin.methods.register_function(
    function=q2_alignment.mafft_add,
    inputs={'alignment': (
            FeatureData[AlignedSequence] |
            FeatureData[AlignedProteinSequence]
            ),
            'sequences': T_GenericSequenceInput},
    parameters={**mafft_params,
                'addfragments': Bool,
                'keeplength': Bool},
    outputs=[('expanded_alignment', T_GenericAlignedSequenceOutput)],
    input_descriptions={'alignment': 'The alignment to which '
                                     'sequences should be added.',
                        'sequences': 'The sequences to be added.'},
    parameter_descriptions={
        **mafft_param_descriptions,
        'addfragments': 'Optimize for the addition of short sequence '
                        'fragments (for example, primer or amplicon '
                        'sequences). If not set, default sequence addition '
                        'is used.',
        'keeplength': 'If selected, the alignment length will be unchanged. '
                      'Any added sequence that would otherwise introduce new '
                      'insertions into the alignment, will have those '
                      'insertions deleted, to preserve original alignment '
                      'length.'},
    output_descriptions={
        'expanded_alignment': 'Alignment containing the provided aligned and '
                              'unaligned sequences.'},
    name='Add sequences to multiple sequence alignment with MAFFT.',
    description='Add new sequences to an existing alignment with MAFFT.',
    citations=[citations['katoh2013mafft']]
)

plugin.methods.register_function(
    function=q2_alignment.mask,
    inputs={'alignment': T_MatchAlignedSequenceType},
    parameters={'max_gap_frequency': Float % Range(0, 1, inclusive_end=True),
                'min_conservation': Float % Range(0, 1, inclusive_end=True)},
    outputs=[('masked_alignment', T_MatchAlignedSequenceType)],
    input_descriptions={'alignment': 'The alignment to be masked.'},
    parameter_descriptions={
        'max_gap_frequency': ('The maximum relative frequency of gap '
                              'characters in a column for the column to be '
                              'retained. This relative frequency must be a '
                              'number between 0.0 and 1.0 (inclusive), where '
                              '0.0 retains only those columns without gap '
                              'characters, and 1.0 retains all columns '
                              'regardless of gap character frequency.'),
        'min_conservation': ('The minimum relative frequency '
                             'of at least one non-gap character in a '
                             'column for that column to be retained. This '
                             'relative frequency must be a number between 0.0 '
                             'and 1.0 (inclusive). For example, if a value of '
                             '0.4 is provided, a column will only be retained '
                             'if it contains at least one character that is '
                             'present in at least 40% of the sequences.')
    },
    output_descriptions={'masked_alignment': 'The masked alignment.'},
    name='Positional conservation and gap filtering.',
    description=("Mask (i.e., filter) unconserved and highly gapped "
                 "columns from an alignment. Default min_conservation was "
                 "chosen to reproduce the mask presented in Lane (1991)."),
    citations=[citations['lane1991']]
)

importlib.import_module("q2_alignment.types._transformers")

# Registrations
plugin.register_semantic_types(
    Orthogroups,
    DNASequences,
    ProteinSequences,
)

plugin.register_semantic_type_to_format(
    semantic_type=Orthogroups[DNASequences],
    artifact_format=GenesDirectoryFormat
)

plugin.register_semantic_type_to_format(
    semantic_type=Orthogroups[AlignedDNASequences],
    artifact_format=GenesDirectoryFormat
)

plugin.register_semantic_type_to_format(
    semantic_type=Orthogroups[ProteinSequences],
    artifact_format=ProteinsDirectoryFormat
)

plugin.register_semantic_type_to_format(
    semantic_type=Orthogroups[AlignedProteinSequences],
    artifact_format=GenesDirectoryFormat
)
