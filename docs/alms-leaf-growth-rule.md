# ALMS Leaf Growth Rule

Internal chain leaves are mechanical.

Rule:
- External audit leaf source = public evidence artifact.
- Internal ALMS chain leaf source = previous sealed receipt manifest at exact git commit.

Operator role:
- choose whether next leaf is EXTERNAL_AUDIT or INTERNAL_CHAIN.
- approve semantic scope.
- sign wallet witness.

Machine role:
- derive source_url.
- compute previous_leaf_hash.
- compute canonical hash.
- generate EAS payload.
- seal receipt after witness.

No manual URL hunting.
No manual hash typing.
No placeholder witnessing.
