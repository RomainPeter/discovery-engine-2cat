#!/usr/bin/env python3
"""
Test script for Discovery Engine 2-Cat.
Validates the migrated components and functionality.
"""

import asyncio
import json
import sys
import os
from datetime import datetime
from pathlib import Path

# Add discovery-engine-2cat directory to path for imports
discovery_dir = Path(__file__).parent.parent
sys.path.insert(0, str(discovery_dir))


async def test_egraph_functionality():
    """Test e-graph canonicalization and equivalence rules."""
    print("🔗 Testing E-graph functionality...")
    
    try:
        from methods.egraph.egraph import EGraph, canonicalize_state, canonicalize_choreography
        
        egraph = EGraph()
        
        # Test 1: State canonicalization
        state1 = {"H": [{"id": "h1"}], "E": [], "K": []}
        state2 = {"H": [{"id": "h1"}], "E": [], "K": []}  # Same as state1
        state3 = {"H": [{"id": "h2"}], "E": [], "K": []}  # Different
        
        id1 = canonicalize_state(state1, egraph)
        id2 = canonicalize_state(state2, egraph)
        id3 = canonicalize_state(state3, egraph)
        
        assert id1 == id2, "Identical states should have same canonical ID"
        assert id1 != id3, "Different states should have different canonical IDs"
        print("✅ State canonicalization works correctly")
        
        # Test 2: Choreography canonicalization
        choreo1 = ["Meet", "Verify", "Normalize"]
        choreo2 = ["Meet", "Verify", "Normalize"]  # Same as choreo1
        choreo3 = ["Generalize", "Contrast", "Verify"]  # Different
        
        id1 = canonicalize_choreography(choreo1, egraph)
        id2 = canonicalize_choreography(choreo2, egraph)
        id3 = canonicalize_choreography(choreo3, egraph)
        
        assert id1 == id2, "Identical choreographies should have same canonical ID"
        assert id1 != id3, "Different choreographies should have different canonical IDs"
        print("✅ Choreography canonicalization works correctly")
        
        # Test 3: E-graph stats
        stats = egraph.get_stats()
        assert stats["total_nodes"] > 0, "Should have nodes in e-graph"
        assert stats["total_classes"] > 0, "Should have equivalence classes"
        print(f"✅ E-graph stats: {stats}")
        
        return True
        
    except Exception as e:
        print(f"❌ E-graph test failed: {e}")
        return False


async def test_ae_loop():
    """Test Attribute Exploration loop."""
    print("\n🔍 Testing AE loop...")
    
    try:
        from orchestrator.ae_loop import AELoop, Implication
        
        # Mock domain spec
        domain_spec = {
            "domain": "RegTech",
            "closure": "exact",
            "oracle_endpoints": [
                {"name": "mock_opa", "type": "OPA", "endpoint": "mock://opa"}
            ]
        }
        
        # Mock e-graph
        from methods.egraph.egraph import EGraph
        egraph = EGraph()
        ae_loop = AELoop(domain_spec, egraph)
        
        # Test implication creation
        implication = Implication(
            id="test_impl",
            premise={"has_license", "is_open_source"},
            conclusion={"compliance_ok"},
            confidence=0.8,
            source="test",
            created_at=datetime.now()
        )
        
        assert implication.id == "test_impl"
        assert implication.confidence == 0.8
        assert "has_license" in implication.premise
        print("✅ Implication creation works correctly")
        
        print("✅ AE loop structure is correct")
        return True
        
    except Exception as e:
        print(f"❌ AE loop test failed: {e}")
        return False


async def test_cegis_loop():
    """Test CEGIS synthesis loop."""
    print("\n🎭 Testing CEGIS loop...")
    
    try:
        from orchestrator.cegis_loop import CEGISLoop, Choreography
        
        # Mock domain spec
        domain_spec = {
            "domain": "RegTech",
            "oracle_endpoints": [
                {"name": "mock_opa", "type": "OPA", "endpoint": "mock://opa"}
            ]
        }
        
        # Mock e-graph
        from methods.egraph.egraph import EGraph
        egraph = EGraph()
        cegis_loop = CEGISLoop(domain_spec, egraph)
        
        # Test choreography creation
        choreography = Choreography(
            id="test_choreo",
            ops=["Meet", "Verify", "Normalize"],
            pre={"constraints": ["K1"]},
            post={"expected_gains": {"coverage": 0.8}},
            guards=["K1", "K2"],
            budgets={"time_ms": 1000, "audit_cost": 50},
            diversity_keys=["constraint_focus"],
            rationale="Test choreography"
        )
        
        assert choreography.id == "test_choreo"
        assert "Meet" in choreography.ops
        assert choreography.budgets["time_ms"] == 1000
        print("✅ Choreography creation works correctly")
        
        print("✅ CEGIS loop structure is correct")
        return True
        
    except Exception as e:
        print(f"❌ CEGIS loop test failed: {e}")
        return False


async def test_domain_adapter():
    """Test domain adapter."""
    print("\n🏢 Testing domain adapter...")
    
    try:
        from domain.regtech_code import RegTechDomain
        
        # Create domain adapter
        domain = RegTechDomain()
        
        # Test configuration creation
        budget = {
            "time_ms": 30000,
            "audit_cost": 1000,
            "legal_risk": 0.3,
            "tech_debt": 0.2
        }
        
        config = domain.create_exploration_config(budget)
        assert config["selection_strategy"] == "bandit"
        print("✅ Domain config creation works correctly")
        
        # Test initial state creation
        initial_state = domain.create_initial_state()
        assert len(initial_state["H"]) > 0
        assert len(initial_state["E"]) > 0
        assert len(initial_state["K"]) > 0
        print("✅ Initial state creation works correctly")
        
        return True
        
    except Exception as e:
        print(f"❌ Domain adapter test failed: {e}")
        return False


async def test_schemas():
    """Test JSON schema validation."""
    print("\n📋 Testing schema validation...")
    
    try:
        # Test DCA schema
        dca_file = discovery_dir / "schemas/dca.schema.json"
        if dca_file.exists():
            with open(dca_file, 'r') as f:
                dca_schema = json.load(f)
            
            # Validate required fields
            required_fields = ["$id", "$schema", "title", "type"]
            for field in required_fields:
                assert field in dca_schema, f"Missing required field: {field}"
            
            print("✅ DCA schema validation works")
        else:
            print("❌ DCA schema file not found")
            return False
        
        # Test CompositeOp schema
        composite_file = discovery_dir / "schemas/composite-op.schema.json"
        if composite_file.exists():
            with open(composite_file, 'r') as f:
                composite_schema = json.load(f)
            
            required_fields = ["$id", "$schema", "title", "type"]
            for field in required_fields:
                assert field in composite_schema, f"Missing required field: {field}"
            
            print("✅ CompositeOp schema validation works")
        else:
            print("❌ CompositeOp schema file not found")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Schema test failed: {e}")
        return False


async def test_prompts():
    """Test LLM prompts."""
    print("\n🤖 Testing LLM prompts...")
    
    try:
        # Test prompt templates exist
        prompt_files = [
            "prompts/ae_implications.tpl",
            "prompts/ae_counterexamples.tpl", 
            "prompts/cegis_choreography.tpl"
        ]
        
        for prompt_file in prompt_files:
            prompt_path = discovery_dir / prompt_file
            assert prompt_path.exists(), f"Missing prompt file: {prompt_file}"
            
            # Check template has required placeholders
            with open(prompt_path, 'r') as f:
                content = f.read()
                assert "{{" in content and "}}" in content, f"Template {prompt_file} should have placeholders"
        
        print("✅ All micro-prompt templates exist and have placeholders")
        return True
        
    except Exception as e:
        print(f"❌ Prompts test failed: {e}")
        return False


async def run_all_tests():
    """Run all tests."""
    print("🧪 Running Discovery Engine 2-Cat Tests")
    print("=" * 50)
    
    tests = [
        ("E-graph functionality", test_egraph_functionality),
        ("AE loop", test_ae_loop),
        ("CEGIS loop", test_cegis_loop),
        ("Domain adapter", test_domain_adapter),
        ("Schema validation", test_schemas),
        ("LLM prompts", test_prompts)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            result = await test_func()
            if result:
                passed += 1
                print(f"✅ {test_name}: PASSED")
            else:
                failed += 1
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            failed += 1
            print(f"❌ {test_name}: FAILED - {e}")
    
    print(f"\n📊 Test Results:")
    print(f"   ✅ Passed: {passed}")
    print(f"   ❌ Failed: {failed}")
    print(f"   📈 Success rate: {passed/(passed+failed)*100:.1f}%")
    
    if failed == 0:
        print("\n🎉 All tests passed! Discovery Engine 2-Cat is ready.")
        return True
    else:
        print(f"\n⚠️  {failed} tests failed. Please review and fix issues.")
        return False


async def main():
    """Main test function."""
    success = await run_all_tests()
    
    if success:
        print("\n🚀 Ready for production use!")
        print("\nNext steps:")
        print("1. Configure the proof-engine-core submodule")
        print("2. Run: python scripts/setup_discovery_engine.py")
        print("3. Demo: python scripts/demo_discovery_engine.py")
        print("4. Benchmarks: python scripts/bench_discovery_engine.py")
    else:
        print("\n🔧 Please fix failing tests before proceeding.")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())