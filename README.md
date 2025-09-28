# Discovery Engine 2-Cat

Orchestrateur 2-cat, AE/CEGIS, e-graphs, bandit/MCTS, domain adapters, benchmarks.

## Architecture

Ce repository contient l'agent de découverte basé sur l'Architecture Unifiée v0.1, utilisant le Proof Engine comme dépendance versionnée.

### Structure

```
discovery-engine-2cat/
├── external/
│   └── proof-engine-core/          # Submodule @ tag v0.1.0
├── orchestrator/                   # Orchestrateur principal
├── methods/                        # Méthodes AE/CEGIS/e-graph
├── domain/                         # Domain adapters
├── schemas/                        # JSON Schemas v0.1
├── bench/                          # Benchmarks + baselines
├── ci/                            # CI/CD + attestations
└── prompts/                       # Micro-prompts LLM
```

### Composants

- **AE (Attribute Exploration)**: Next-closure algorithm avec oracle Verifier
- **CEGIS**: Counter-Example Guided Inductive Synthesis
- **E-graphs**: Canonicalisation et anti-redondance structurelle
- **Sélection**: Bandit contextuel, MCTS, Pareto
- **Domain Adapters**: RegTech/Code, etc.

### Utilisation

```bash
# Tests
python scripts/test_discovery_engine.py

# Démo
python scripts/demo_discovery_engine.py

# Benchmarks
python scripts/bench_discovery_engine.py
```

### Dépendances

- **proof-engine-core**: Noyau stable (PCAP, runner hermétique, attestations)
- **Python 3.9+**: Runtime
- **OPA**: Oracle pour vérification
- **Static Analysis**: Outils d'analyse statique

### Versioning

- **discovery-engine**: v0.x (exploration et orchestration)
- **proof-engine-core**: v0.x (noyau stable)
- Compatibilité: `proof-engine-core>=0.1.0,<0.2.0`

## Développement

### Migration depuis proof-engine-for-code

Ce repository a été créé en migrant les composants d'exploration depuis le Proof Engine principal pour permettre un développement indépendant et accéléré.

### Garde-fous

- Aucune modification directe de `proof-engine-core`
- Toute évolution du core → PR sur proof-engine-core → nouveau tag → bump submodule
- Attestations distinctes par repository
- Versionnage coordonné avec contraintes de compatibilité

## License

Voir LICENSE pour les détails.
