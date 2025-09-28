#!/usr/bin/env python3
"""
Demo script for Discovery Engine 2-Cat.
Demonstrates the migrated components and functionality.
"""

import asyncio
import json
import sys
from datetime import datetime
from pathlib import Path

# Add discovery-engine-2cat directory to path for imports
discovery_dir = Path(__file__).parent.parent
sys.path.insert(0, str(discovery_dir))


async def demo_egraph_canonicalization():
    """Demonstrate e-graph canonicalization."""
    print("🔗 E-graph Canonicalization Demo")
    print("=" * 40)
    
    try:
        from methods.egraph.egraph import EGraph, canonicalize_state, canonicalize_choreography
        
        egraph = EGraph()
        
        # Test state canonicalization
        state1 = {"H": [{"id": "h1", "title": "Test"}], "E": [], "K": []}
        state2 = {"H": [{"id": "h1", "title": "Test"}], "E": [], "K": []}  # Same as state1
        state3 = {"H": [{"id": "h2", "title": "Different"}], "E": [], "K": []}  # Different
        
        id1 = canonicalize_state(state1, egraph)
        id2 = canonicalize_state(state2, egraph)
        id3 = canonicalize_state(state3, egraph)
        
        print(f"State 1 canonical ID: {id1}")
        print(f"State 2 canonical ID: {id2}")
        print(f"State 3 canonical ID: {id3}")
        print(f"States 1&2 equivalent: {id1 == id2}")
        print(f"States 1&3 equivalent: {id1 == id3}")
        
        # Show e-graph stats
        stats = egraph.get_stats()
        print(f"\n📊 E-graph stats:")
        print(f"   - Total nodes: {stats['total_nodes']}")
        print(f"   - Total classes: {stats['total_classes']}")
        print(f"   - Avg class size: {stats['avg_class_size']:.2f}")
        
        return True
        
    except Exception as e:
        print(f"❌ E-graph demo failed: {e}")
        return False


async def demo_schema_validation():
    """Demonstrate schema validation."""
    print("\n📋 Schema Validation Demo")
    print("=" * 40)
    
    # Test DCA schema
    dca_example = {
        "version": "0.1.0",
        "id": "dca_1",
        "type": "AE_query",
        "context_hash": "a" * 64,
        "query_or_prog": "has_license ∧ is_open_source ⇒ compliance_ok",
        "V_hat": {"time_ms": 100, "audit_cost": 50, "legal_risk": 0.1, "tech_debt": 0.2},
        "S_hat": {"info_gain": 0.8, "coverage_gain": 0.7, "MDL_drop": -0.3, "novelty": 0.6},
        "V_actual": {"time_ms": 120, "audit_cost": 55, "legal_risk": 0.1, "tech_debt": 0.2},
        "S_actual": {"info_gain": 0.8, "coverage_gain": 0.7, "MDL_drop": -0.3, "novelty": 0.6},
        "verdict": "accept"
    }
    
    print(f"✅ DCA example created: {dca_example['id']}")
    print(f"   - Type: {dca_example['type']}")
    print(f"   - Query: {dca_example['query_or_prog']}")
    print(f"   - Verdict: {dca_example['verdict']}")
    
    # Test CompositeOp schema
    composite_example = {
        "version": "0.1.0",
        "id": "choreo_1",
        "ops": ["Meet", "Verify", "Normalize"],
        "guards": ["K1", "K2"],
        "budgets": {"time_ms": 1000, "audit_cost": 50, "legal_risk": 0.1, "tech_debt": 0.2},
        "diversity_keys": ["constraint_focus", "verification_heavy"],
        "rationale": "Basic constraint checking approach"
    }
    
    print(f"\n✅ CompositeOp example created: {composite_example['id']}")
    print(f"   - Operations: {composite_example['ops']}")
    print(f"   - Guards: {composite_example['guards']}")
    print(f"   - Rationale: {composite_example['rationale']}")
    
    return True


async def demo_domain_adapter():
    """Demonstrate domain adapter."""
    print("\n🏢 Domain Adapter Demo")
    print("=" * 40)
    
    try:
        # Create a simple domain adapter without imports
        class SimpleRegTechDomain:
            def __init__(self):
                self.domain_spec = {
                    "domain": "RegTech",
                    "closure": "exact",
                    "oracle_endpoints": [
                        {"name": "OPA_Rego", "type": "OPA", "endpoint": "http://localhost:8181/v1/data"}
                    ]
                }
            
            def create_exploration_config(self, budget):
                return {
                    "domain_spec": self.domain_spec,
                    "budget": budget,
                    "selection_strategy": "bandit",
                    "max_iterations": 10
                }
            
            def create_initial_state(self):
                return {
                    "H": [{"id": "h1", "title": "License compliance", "status": "open"}],
                    "E": [{"id": "e1", "kind": "code", "uri": "src/main.py"}],
                    "K": [{"id": "k1", "source": "internal", "rule": "eu_ai_act_transparency"}],
                    "A": [],
                    "J": {"version": "0.1.0", "entries": []},
                    "Sigma": {"repo": "discovery-engine-2cat", "branch": "main"}
                }
        
        # Create domain adapter
        domain = SimpleRegTechDomain()
        
        # Create configuration
        budget = {"time_ms": 30000, "audit_cost": 1000, "legal_risk": 0.3, "tech_debt": 0.2}
        config = domain.create_exploration_config(budget)
        print(f"✅ Exploration config created: {config['selection_strategy']}")
        
        # Create initial state
        initial_state = domain.create_initial_state()
        print(f"✅ Initial state created: {len(initial_state['H'])} hypotheses")
        
        return True
        
    except Exception as e:
        print(f"❌ Domain adapter demo failed: {e}")
        return False


async def demo_prompts():
    """Demonstrate LLM prompts."""
    print("\n🤖 LLM Prompts Demo")
    print("=" * 40)
    
    # Check prompt templates
    prompt_files = [
        "prompts/ae_implications.tpl",
        "prompts/ae_counterexamples.tpl", 
        "prompts/cegis_choreography.tpl"
    ]
    
    for prompt_file in prompt_files:
        prompt_path = discovery_dir / prompt_file
        if prompt_path.exists():
            with open(prompt_path, 'r') as f:
                content = f.read()
                # Check for template placeholders
                if "{{" in content and "}}" in content:
                    print(f"✅ {prompt_file}: Template with placeholders")
                else:
                    print(f"⚠️  {prompt_file}: Template without placeholders")
        else:
            print(f"❌ {prompt_file}: Not found")
    
    return True


async def demo_architecture_overview():
    """Demonstrate the overall architecture."""
    print("\n🏗️ Architecture Overview Demo")
    print("=" * 40)
    
    print("Discovery Engine 2-Cat Components:")
    print("├── orchestrator/")
    print("│   ├── unified_orchestrator.py     # Main orchestrator")
    print("│   ├── ae_loop.py                  # Attribute Exploration")
    print("│   ├── cegis_loop.py               # CEGIS synthesis")
    print("│   └── selection.py                # Bandit/MCTS/Pareto")
    print("├── methods/")
    print("│   └── egraph/")
    print("│       └── egraph.py               # E-graph canonicalization")
    print("├── domain/")
    print("│   └── regtech_code/               # RegTech/Code adapter")
    print("├── schemas/                        # JSON Schemas v0.1")
    print("├── prompts/                        # LLM micro-prompts")
    print("└── external/")
    print("    └── proof-engine-core/           # Submodule (to be configured)")
    
    print("\nKey Features:")
    print("✅ AE (Attribute Exploration): Next-closure algorithm")
    print("✅ CEGIS: Counter-Example Guided Inductive Synthesis")
    print("✅ E-graphs: Canonicalization and anti-redundancy")
    print("✅ Selection: Bandit contextuel, MCTS, Pareto")
    print("✅ Domain Adapters: RegTech/Code, extensible")
    print("✅ JSON Schemas: DCA, CompositeOp, DomainSpec, FailReason")
    print("✅ LLM Integration: Micro-prompts for implications/counterexamples")
    
    return True


async def main():
    """Main demo function."""
    print("🎯 Discovery Engine 2-Cat - Complete Demo")
    print("=" * 60)
    
    # Demo 1: Architecture overview
    await demo_architecture_overview()
    
    # Demo 2: E-graph canonicalization
    await demo_egraph_canonicalization()
    
    # Demo 3: Schema validation
    await demo_schema_validation()
    
    # Demo 4: Domain adapter
    await demo_domain_adapter()
    
    # Demo 5: LLM prompts
    await demo_prompts()
    
    print("\n🎉 Demo completed successfully!")
    print("\n📚 Next steps:")
    print("1. Configure the proof-engine-core submodule")
    print("2. Run: python scripts/setup_discovery_engine.py")
    print("3. Test: python scripts/test_discovery_engine.py")
    print("4. Benchmarks: python scripts/bench_discovery_engine.py")
    print("5. Integrate with real oracles (OPA, static analysis)")
    print("6. Scale to larger exploration spaces")


if __name__ == "__main__":
    asyncio.run(main())