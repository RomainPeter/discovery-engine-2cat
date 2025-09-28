# Migration Guide: Proof Engine → Discovery Engine 2-Cat

## Vue d'ensemble

Ce guide documente la migration des composants d'exploration depuis `proof-engine-for-code` vers `discovery-engine-2cat`, permettant un développement indépendant et accéléré de l'agent de découverte.

## 🎯 Objectifs de la migration

### **Séparation des responsabilités**
- **proof-engine-core** : Noyau stable (PCAP, runner hermétique, attestations, oracles)
- **discovery-engine-2cat** : Exploration et orchestration (AE/CEGIS, e-graphs, bandit/MCTS)

### **Avantages**
- ✅ **Éviter les régressions** : Pin exact sur version stable du Proof Engine
- ✅ **Accélérer l'itération** : Développement indépendant de l'exploration
- ✅ **Verrouiller la repro** : Hash de commit garanti via sous-module
- ✅ **CI/CD ciblé** : Jobs spécifiques par composant
- ✅ **Releases indépendantes** : SEMVER distinctes

## 📁 Structure de migration

### **Composants migrés vers discovery-engine-2cat**

```
discovery-engine-2cat/
├── orchestrator/                    # Depuis proofengine/orchestrator/
│   ├── unified_orchestrator.py     # Orchestrateur principal
│   ├── ae_loop.py                  # Attribute Exploration
│   ├── cegis_loop.py               # CEGIS synthesis
│   └── selection.py                # Bandit/MCTS/Pareto
├── methods/                        # Depuis proofengine/core/ + planner/
│   ├── ae/                         # Méthodes AE
│   ├── cegis/                      # Méthodes CEGIS
│   └── egraph/                     # E-graph canonicalization
├── schemas/                        # Depuis specs/v0.1/
│   ├── dca.schema.json             # Decision Context Artifact
│   ├── composite-op.schema.json    # CompositeOp/Choreography
│   ├── domain-spec.schema.json     # DomainSpec
│   ├── failreason-extended.schema.json # FailReason étendu
│   └── domain-spec-regtech-code.json # Instanciation RegTech/Code
├── prompts/                        # Depuis prompts/
│   ├── ae_implications.tpl         # Micro-prompt implications
│   ├── ae_counterexamples.tpl      # Micro-prompt contre-exemples
│   └── cegis_choreography.tpl      # Micro-prompt chorégraphies
├── domain/                         # Nouveau
│   └── regtech_code/               # Domain adapters
├── bench/                          # Nouveau
│   └── (benchmarking infrastructure)
├── ci/                            # Nouveau
│   └── (CI/CD + attestations)
└── external/                      # Nouveau
    └── proof-engine-core/         # Sous-module Git
```

### **Composants conservés dans proof-engine-core**

```
proof-engine-core/
├── proofengine/
│   ├── verifier/                   # OPA, static analysis
│   ├── runner/                     # Runner hermétique
│   ├── controller/                 # PCAP, attestations
│   └── core/                       # Schémas de base (X, PCAP, Journal)
├── specs/v0.1/                     # Schémas de base uniquement
└── ...
```

## 🔄 Processus de migration

### **Étape 1: Préparation**
```bash
# Dans proof-engine-for-code
python scripts/migrate_to_discovery_engine.py
```

### **Étape 2: Configuration du nouveau repository**
```bash
cd discovery-engine-2cat
python scripts/setup_discovery_engine.py
```

### **Étape 3: Configuration du sous-module**
```bash
# Ajouter le sous-module proof-engine-core
git submodule add <proof-engine-core-url> external/proof-engine-core
cd external/proof-engine-core
git checkout v0.1.0  # Pin sur version stable
cd ../..
```

### **Étape 4: Configuration Git**
```bash
git add .
git commit -m "Initial commit: Discovery Engine 2-Cat"
git remote add origin <discovery-engine-2cat-url>
git push -u origin main
```

## 🔗 Intégration avec Proof Engine

### **Dépendance par sous-module Git**

```bash
# Dans discovery-engine-2cat
external/proof-engine-core/          # Sous-module @ tag v0.1.0
```

**Avantages :**
- ✅ Pin exact sur version stable
- ✅ Visibilité complète du code source
- ✅ Zéro dépendance sur registre privé
- ✅ Reproductibilité garantie

**Inconvénients :**
- ⚠️ Friction du sous-module (peut être migré plus tard)

### **Migration future vers package versionné**

```python
# requirements.txt
proof-engine-core>=0.1.0,<0.2.0
proof-engine-schemas>=0.1.0,<0.2.0
```

**Avantages :**
- ✅ Intégration simple
- ✅ Updates contrôlés par bump de version
- ✅ Gestion des dépendances standardisée

## 🛡️ Garde-fous

### **Isolation stricte**
- ❌ **Aucune modification directe** de `proof-engine-core` depuis discovery
- ✅ **Toute évolution du core** → PR sur proof-engine-core → nouveau tag → bump submodule

### **Attestations distinctes**
- Chaque repository a ses propres attestations
- Provenance in-toto inclut le hash du submodule/tag
- Versionnage coordonné : `pe-core v0.x`, `discovery v0.x`

### **Contraintes de compatibilité**
```yaml
# Dans discovery-engine-2cat/requirements.txt
proof-engine-core>=0.1.0,<0.2.0
```

## 📊 Comparaison avant/après

### **Avant (proof-engine-for-code monolithique)**
```
proof-engine-for-code/
├── proofengine/
│   ├── orchestrator/               # Exploration
│   ├── verifier/                   # Noyau stable
│   ├── runner/                     # Noyau stable
│   └── core/                       # Mélangé
├── specs/                          # Tous les schémas
└── ...
```

**Problèmes :**
- Couplage fort entre exploration et noyau
- Risque de régression lors des changements
- Releases coordonnées complexes
- CI/CD monolithique

### **Après (discovery-engine-2cat + proof-engine-core)**
```
discovery-engine-2cat/              # Exploration
├── orchestrator/                   # AE/CEGIS
├── methods/                        # E-graphs, bandit/MCTS
├── domain/                         # Domain adapters
└── external/proof-engine-core/     # Sous-module

proof-engine-core/                  # Noyau stable
├── proofengine/
│   ├── verifier/                   # OPA, static analysis
│   ├── runner/                     # Runner hermétique
│   └── controller/                 # PCAP, attestations
└── specs/                          # Schémas de base
```

**Avantages :**
- ✅ Séparation claire des responsabilités
- ✅ Développement indépendant
- ✅ Releases indépendantes
- ✅ CI/CD ciblé
- ✅ Reproductibilité garantie

## 🚀 Utilisation

### **Commandes de base**
```bash
# Tests
make test

# Démo
make demo

# Benchmarks
make bench

# Mise à jour du sous-module
make submodule-update
```

### **Développement**
```bash
# Configuration initiale
python scripts/setup_discovery_engine.py

# Tests complets
python scripts/test_discovery_engine.py

# Démo complète
python scripts/demo_discovery_engine.py
```

## 🔄 Workflow de développement

### **Modification du noyau (proof-engine-core)**
1. Créer une branche dans `proof-engine-core`
2. Implémenter les changements
3. Créer une PR et la merger
4. Créer un nouveau tag (ex: v0.1.1)
5. Dans `discovery-engine-2cat` : `git submodule update --remote`

### **Modification de l'exploration (discovery-engine-2cat)**
1. Créer une branche dans `discovery-engine-2cat`
2. Implémenter les changements
3. Tester avec la version pinée de `proof-engine-core`
4. Créer une PR et la merger

## 📈 Métriques de succès

### **Reproductibilité**
- ✅ Hash de commit garanti via sous-module
- ✅ Attestations distinctes par repository
- ✅ Provenance in-toto inclut le hash du submodule

### **Développement**
- ✅ Temps de CI réduit (jobs ciblés)
- ✅ Releases indépendantes
- ✅ Éviter les régressions

### **Maintenance**
- ✅ Séparation claire des responsabilités
- ✅ Évolution indépendante des composants
- ✅ Gestion des dépendances simplifiée

## 🎯 Prochaines étapes

1. **Migration complète** : Finaliser la migration de tous les composants
2. **Tests d'intégration** : Valider le fonctionnement avec le sous-module
3. **CI/CD** : Configurer les pipelines pour les deux repositories
4. **Documentation** : Compléter la documentation technique
5. **Benchmarks** : Implémenter les benchmarks de performance

## 📚 Références

- [Architecture Unifiée v0.1](../docs/ARCHITECTURE_UNIFIEE_V01.md)
- [Proof Engine Core](../external/proof-engine-core/README.md)
- [Discovery Engine 2-Cat](../README.md)
- [Git Submodules Guide](https://git-scm.com/book/en/v2/Git-Tools-Submodules)
