#!/usr/bin/env python3
"""
Script de configuration pour discovery-engine-2cat.
Initialise le repository avec les dépendances et configurations.
"""

import os
import subprocess
import sys
from pathlib import Path


def run_command(command, cwd=None):
    """Exécuter une commande et retourner le résultat."""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            cwd=cwd, 
            capture_output=True, 
            text=True, 
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed: {command}")
        print(f"Error: {e.stderr}")
        return None


def setup_git_repository():
    """Initialiser le repository Git."""
    print("🔧 Setting up Git repository...")
    
    # Initialiser Git
    if not Path(".git").exists():
        run_command("git init")
        print("✅ Git repository initialized")
    else:
        print("✅ Git repository already exists")
    
    return True


def setup_submodule():
    """Configurer le sous-module proof-engine-core."""
    print("🔗 Setting up proof-engine-core submodule...")
    
    # URL du repository proof-engine-core (à adapter selon votre setup)
    proof_engine_url = "https://github.com/your-org/proof-engine-core.git"
    
    # Ajouter le sous-module
    result = run_command(f"git submodule add {proof_engine_url} external/proof-engine-core")
    if result is not None:
        print("✅ Submodule added")
        
        # Checkout sur la version stable
        run_command("cd external/proof-engine-core && git checkout v0.1.0")
        print("✅ Submodule pinned to v0.1.0")
    else:
        print("⚠️  Submodule setup failed - please configure manually")
    
    return True


def setup_python_environment():
    """Configurer l'environnement Python."""
    print("🐍 Setting up Python environment...")
    
    # Créer l'environnement virtuel
    if not Path(".venv").exists():
        run_command("python -m venv .venv")
        print("✅ Virtual environment created")
    else:
        print("✅ Virtual environment already exists")
    
    # Installer les dépendances
    if os.name == 'nt':  # Windows
        activate_cmd = ".venv\\Scripts\\activate"
    else:  # Unix/Linux
        activate_cmd = "source .venv/bin/activate"
    
    install_cmd = f"{activate_cmd} && pip install -U pip && pip install -r requirements.txt"
    result = run_command(install_cmd)
    
    if result is not None:
        print("✅ Dependencies installed")
    else:
        print("⚠️  Dependency installation failed")
    
    return True


def create_initial_commit():
    """Créer le commit initial."""
    print("📝 Creating initial commit...")
    
    # Ajouter tous les fichiers
    run_command("git add .")
    
    # Créer le commit
    commit_message = """Initial commit: Discovery Engine 2-Cat

- Migrated from proof-engine-for-code
- Architecture Unifiée v0.1 implementation
- AE/CEGIS loops with e-graph canonicalization
- Bandit/MCTS selection strategies
- RegTech/Code domain adapter
- JSON Schemas v0.1
- Micro-prompts for LLM integration

Components:
- orchestrator/: Unified orchestrator with AE/CEGIS
- methods/: AE, CEGIS, e-graph implementations
- domain/: Domain adapters (RegTech/Code)
- schemas/: JSON Schemas v0.1
- prompts/: LLM micro-prompts
- bench/: Benchmarking infrastructure
- ci/: CI/CD configuration

Dependencies:
- proof-engine-core (submodule @ v0.1.0)
- Python 3.9+ with async support
- OPA for policy verification
- Static analysis tools
"""
    
    run_command(f'git commit -m "{commit_message}"')
    print("✅ Initial commit created")
    
    return True


def create_github_workflow():
    """Créer le workflow GitHub Actions."""
    print("🔄 Creating GitHub Actions workflow...")
    
    workflow_content = """name: Discovery Engine 2-Cat CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.9, 3.10, 3.11]
    
    steps:
    - uses: actions/checkout@v3
      with:
        submodules: recursive
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python scripts/test_discovery_engine.py
    
    - name: Run demo
      run: |
        python scripts/demo_discovery_engine.py
    
    - name: Run benchmarks
      run: |
        python scripts/bench_discovery_engine.py

  security:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
      with:
        submodules: recursive
    
    - name: Run security scan
      run: |
        pip install safety
        safety check
    
    - name: Run bandit security linter
      run: |
        pip install bandit
        bandit -r . -f json -o bandit-report.json

  attestation:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
      with:
        submodules: recursive
    
    - name: Generate attestation
      run: |
        python scripts/generate_attestation.py
    
    - name: Sign attestation
      run: |
        cosign sign-blob attestation.json --key .github/security/cosign.key
"""
    
    workflow_dir = Path(".github/workflows")
    workflow_dir.mkdir(parents=True, exist_ok=True)
    
    workflow_file = workflow_dir / "ci.yml"
    with open(workflow_file, 'w') as f:
        f.write(workflow_content)
    
    print("✅ GitHub Actions workflow created")
    return True


def create_domain_adapter():
    """Créer l'adaptateur de domaine RegTech/Code."""
    print("🏢 Creating RegTech/Code domain adapter...")
    
    domain_content = """#!/usr/bin/env python3
\"\"\"
RegTech/Code Domain Adapter for Discovery Engine 2-Cat.
Implements domain-specific logic for regulatory technology and code analysis.
\"\"\"

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import json
from pathlib import Path

from ..orchestrator.unified_orchestrator import UnifiedOrchestrator, ExplorationConfig
from ..methods.egraph.egraph import EGraph, canonicalize_state


class RegTechDomain:
    \"\"\"Domain adapter for RegTech/Code scenarios.\"\"\"
    
    def __init__(self, config_path: str = "domain/regtech_code/config.yaml"):
        self.config_path = config_path
        self.domain_spec = self._load_domain_spec()
        self.egraph = EGraph()
    
    def _load_domain_spec(self) -> Dict[str, Any]:
        \"\"\"Charger la spécification du domaine.\"\"\"
        spec_file = Path("schemas/domain-spec-regtech-code.json")
        if spec_file.exists():
            with open(spec_file, 'r') as f:
                return json.load(f)
        else:
            return self._get_default_domain_spec()
    
    def _get_default_domain_spec(self) -> Dict[str, Any]:
        \"\"\"Spécification par défaut du domaine RegTech/Code.\"\"\"
        return {
            "domain": "RegTech",
            "closure": "exact",
            "oracle_endpoints": [
                {
                    "name": "OPA_Rego",
                    "type": "OPA",
                    "endpoint": "http://localhost:8181/v1/data",
                    "timeout_ms": 5000
                },
                {
                    "name": "Static_Analysis",
                    "type": "static_analysis",
                    "endpoint": "local://tools/static_analysis",
                    "timeout_ms": 10000
                }
            ],
            "cost_model": {
                "dimensions": ["time_ms", "audit_cost", "legal_risk", "tech_debt"],
                "units": {
                    "time_ms": "milliseconds",
                    "audit_cost": "USD",
                    "legal_risk": "risk_score_0_1",
                    "tech_debt": "debt_score_0_1"
                }
            }
        }
    
    def create_exploration_config(self, budget: Dict[str, float]) -> ExplorationConfig:
        \"\"\"Créer une configuration d'exploration pour le domaine RegTech/Code.\"\"\"
        return ExplorationConfig(
            domain_spec=self.domain_spec,
            budget=budget,
            diversity_config={
                "target_diversity": 0.8,
                "min_novelty": 0.6
            },
            selection_strategy="bandit",
            max_iterations=10,
            convergence_threshold=0.1
        )
    
    def create_initial_state(self, 
                           hypotheses: List[str] = None,
                           evidence: List[str] = None,
                           constraints: List[str] = None) -> Dict[str, Any]:
        \"\"\"Créer un état initial pour l'exploration RegTech/Code.\"\"\"
        if hypotheses is None:
            hypotheses = [
                "License compliance required",
                "Security vulnerabilities must be patched",
                "API changes need version bump"
            ]
        
        if evidence is None:
            evidence = [
                "src/main.py",
                "requirements.txt",
                "LICENSE"
            ]
        
        if constraints is None:
            constraints = [
                "eu_ai_act_transparency",
                "nist_rmf_security",
                "semver_compliance"
            ]
        
        return {
            "H": [{"id": f"h{i}", "title": h, "status": "open"} 
                  for i, h in enumerate(hypotheses)],
            "E": [{"id": f"e{i}", "kind": "code", "uri": e} 
                  for i, e in enumerate(evidence)],
            "K": [{"id": f"k{i}", "source": "internal", "rule": c} 
                  for i, c in enumerate(constraints)],
            "A": [],
            "J": {"version": "0.1.0", "entries": []},
            "Sigma": {
                "repo": "discovery-engine-2cat",
                "branch": "main",
                "tooling": {"python": "3.9", "llm_model": "gpt-4"}
            }
        }


def main():
    \"\"\"Démonstration de l'adaptateur de domaine RegTech/Code.\"\"\"
    print("🏢 RegTech/Code Domain Adapter Demo")
    print("=" * 40)
    
    # Créer l'adaptateur
    domain = RegTechDomain()
    
    # Créer la configuration d'exploration
    budget = {
        "time_ms": 30000,
        "audit_cost": 1000,
        "legal_risk": 0.3,
        "tech_debt": 0.2
    }
    
    config = domain.create_exploration_config(budget)
    print(f"✅ Exploration config created: {config.selection_strategy}")
    
    # Créer l'état initial
    initial_state = domain.create_initial_state()
    print(f"✅ Initial state created: {len(initial_state['H'])} hypotheses")
    
    # Canonicaliser l'état
    canonical_id = canonicalize_state(initial_state, domain.egraph)
    print(f"✅ State canonicalized: {canonical_id}")
    
    print("\\n🎉 RegTech/Code domain adapter ready!")


if __name__ == "__main__":
    main()
"""
    
    domain_file = Path("domain/regtech_code/__init__.py")
    domain_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(domain_file, 'w') as f:
        f.write(domain_content)
    
    print("✅ RegTech/Code domain adapter created")
    return True


def main():
    """Fonction principale de configuration."""
    
    print("🚀 Discovery Engine 2-Cat Setup")
    print("=" * 40)
    
    # Vérifier qu'on est dans le bon répertoire
    if not Path("discovery-engine-2cat").exists():
        print("❌ Please run this script from the parent directory")
        return False
    
    # Changer vers le répertoire discovery-engine-2cat
    os.chdir("discovery-engine-2cat")
    
    # 1. Configuration Git
    setup_git_repository()
    
    # 2. Configuration du sous-module
    setup_submodule()
    
    # 3. Configuration Python
    setup_python_environment()
    
    # 4. Création du workflow CI
    create_github_workflow()
    
    # 5. Création de l'adaptateur de domaine
    create_domain_adapter()
    
    # 6. Commit initial
    create_initial_commit()
    
    print("\n🎉 Discovery Engine 2-Cat setup completed!")
    print("\n📋 Next steps:")
    print("1. Configure the proof-engine-core submodule URL")
    print("2. git remote add origin <discovery-engine-2cat-url>")
    print("3. git push -u origin main")
    print("4. Enable GitHub Actions")
    print("5. Configure secrets for attestation signing")
    
    return True


if __name__ == "__main__":
    main()

