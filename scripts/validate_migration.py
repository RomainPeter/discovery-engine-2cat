#!/usr/bin/env python3
"""
Script de validation de la migration vers discovery-engine-2cat.
Vérifie que tous les composants ont été correctement migrés.
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Any


def check_file_exists(file_path: str, description: str) -> bool:
    """Vérifier qu'un fichier existe."""
    if Path(file_path).exists():
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ {description}: {file_path} - NOT FOUND")
        return False


def check_directory_structure() -> bool:
    """Vérifier la structure des dossiers."""
    print("📁 Checking directory structure...")
    
    required_dirs = [
        "orchestrator",
        "methods/ae",
        "methods/cegis", 
        "methods/egraph",
        "domain/regtech_code",
        "schemas",
        "prompts",
        "bench",
        "ci",
        "tests",
        "docs",
        "scripts",
        "external/proof-engine-core"
    ]
    
    all_exist = True
    for directory in required_dirs:
        if Path(directory).exists():
            print(f"✅ Directory: {directory}")
        else:
            print(f"❌ Directory: {directory} - NOT FOUND")
            all_exist = False
    
    return all_exist


def check_orchestrator_components() -> bool:
    """Vérifier les composants de l'orchestrateur."""
    print("\n🎭 Checking orchestrator components...")
    
    orchestrator_files = [
        ("orchestrator/unified_orchestrator.py", "Unified Orchestrator"),
        ("orchestrator/ae_loop.py", "AE Loop"),
        ("orchestrator/cegis_loop.py", "CEGIS Loop"),
        ("orchestrator/selection.py", "Selection Strategies")
    ]
    
    all_exist = True
    for file_path, description in orchestrator_files:
        if not check_file_exists(file_path, description):
            all_exist = False
    
    return all_exist


def check_methods_components() -> bool:
    """Vérifier les composants des méthodes."""
    print("\n🔬 Checking methods components...")
    
    methods_files = [
        ("methods/egraph/egraph.py", "E-graph Implementation")
    ]
    
    all_exist = True
    for file_path, description in methods_files:
        if not check_file_exists(file_path, description):
            all_exist = False
    
    return all_exist


def check_schemas() -> bool:
    """Vérifier les schémas JSON."""
    print("\n📋 Checking JSON schemas...")
    
    schema_files = [
        ("schemas/dca.schema.json", "DCA Schema"),
        ("schemas/composite-op.schema.json", "CompositeOp Schema"),
        ("schemas/domain-spec.schema.json", "DomainSpec Schema"),
        ("schemas/failreason-extended.schema.json", "FailReason Extended Schema"),
        ("schemas/domain-spec-regtech-code.json", "RegTech/Code Domain Spec")
    ]
    
    all_exist = True
    for file_path, description in schema_files:
        if not check_file_exists(file_path, description):
            all_exist = False
    
    return all_exist


def check_prompts() -> bool:
    """Vérifier les micro-prompts."""
    print("\n🤖 Checking LLM prompts...")
    
    prompt_files = [
        ("prompts/ae_implications.tpl", "AE Implications Prompt"),
        ("prompts/ae_counterexamples.tpl", "AE Counterexamples Prompt"),
        ("prompts/cegis_choreography.tpl", "CEGIS Choreography Prompt")
    ]
    
    all_exist = True
    for file_path, description in prompt_files:
        if not check_file_exists(file_path, description):
            all_exist = False
    
    return all_exist


def check_scripts() -> bool:
    """Vérifier les scripts."""
    print("\n📜 Checking scripts...")
    
    script_files = [
        ("scripts/test_discovery_engine.py", "Test Script"),
        ("scripts/demo_discovery_engine.py", "Demo Script"),
        ("scripts/setup_discovery_engine.py", "Setup Script"),
        ("scripts/validate_migration.py", "Validation Script")
    ]
    
    all_exist = True
    for file_path, description in script_files:
        if not check_file_exists(file_path, description):
            all_exist = False
    
    return all_exist


def check_config_files() -> bool:
    """Vérifier les fichiers de configuration."""
    print("\n⚙️ Checking configuration files...")
    
    config_files = [
        ("README.md", "README"),
        (".gitignore", "Git Ignore"),
        ("requirements.txt", "Requirements"),
        ("Makefile", "Makefile"),
        ("configs/unified_architecture.yaml", "Unified Architecture Config")
    ]
    
    all_exist = True
    for file_path, description in config_files:
        if not check_file_exists(file_path, description):
            all_exist = False
    
    return all_exist


def check_imports() -> bool:
    """Vérifier que les imports sont corrects."""
    print("\n🔗 Checking imports...")
    
    # Vérifier les imports dans les fichiers principaux
    import_checks = [
        {
            "file": "orchestrator/unified_orchestrator.py",
            "imports": ["from ..methods.egraph.egraph import EGraph", "from .ae_loop import AELoop"]
        },
        {
            "file": "orchestrator/ae_loop.py", 
            "imports": ["from ..methods.egraph.egraph import EGraph"]
        },
        {
            "file": "orchestrator/cegis_loop.py",
            "imports": ["from ..methods.egraph.egraph import EGraph"]
        }
    ]
    
    all_correct = True
    for check in import_checks:
        file_path = Path(check["file"])
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            for import_stmt in check["imports"]:
                if import_stmt in content:
                    print(f"✅ Import found in {check['file']}: {import_stmt}")
                else:
                    print(f"❌ Import missing in {check['file']}: {import_stmt}")
                    all_correct = False
        else:
            print(f"❌ File not found: {check['file']}")
            all_correct = False
    
    return all_correct


def check_schema_validation() -> bool:
    """Vérifier que les schémas JSON sont valides."""
    print("\n📋 Checking schema validation...")
    
    schema_files = [
        "schemas/dca.schema.json",
        "schemas/composite-op.schema.json",
        "schemas/domain-spec.schema.json",
        "schemas/failreason-extended.schema.json"
    ]
    
    all_valid = True
    for schema_file in schema_files:
        if Path(schema_file).exists():
            try:
                with open(schema_file, 'r', encoding='utf-8') as f:
                    schema = json.load(f)
                
                # Vérifier les champs requis
                required_fields = ["$id", "$schema", "title", "type"]
                for field in required_fields:
                    if field not in schema:
                        print(f"❌ Schema {schema_file} missing required field: {field}")
                        all_valid = False
                    else:
                        print(f"✅ Schema {schema_file} has field: {field}")
                
            except json.JSONDecodeError as e:
                print(f"❌ Schema {schema_file} is not valid JSON: {e}")
                all_valid = False
        else:
            print(f"❌ Schema file not found: {schema_file}")
            all_valid = False
    
    return all_valid


def check_domain_adapter() -> bool:
    """Vérifier l'adaptateur de domaine."""
    print("\n🏢 Checking domain adapter...")
    
    domain_files = [
        ("domain/regtech_code/__init__.py", "RegTech Domain Adapter")
    ]
    
    all_exist = True
    for file_path, description in domain_files:
        if not check_file_exists(file_path, description):
            all_exist = False
    
    return all_exist


def run_basic_tests() -> bool:
    """Exécuter des tests de base."""
    print("\n🧪 Running basic tests...")
    
    try:
        # Test d'import des modules principaux
        import sys
        sys.path.insert(0, '.')
        
        # Test d'import de l'orchestrateur
        try:
            from orchestrator.unified_orchestrator import UnifiedOrchestrator
            print("✅ UnifiedOrchestrator import successful")
        except ImportError as e:
            print(f"❌ UnifiedOrchestrator import failed: {e}")
            return False
        
        # Test d'import de l'e-graph
        try:
            from methods.egraph.egraph import EGraph
            print("✅ EGraph import successful")
        except ImportError as e:
            print(f"❌ EGraph import failed: {e}")
            return False
        
        # Test d'import des schémas
        try:
            import json
            with open("schemas/dca.schema.json", 'r') as f:
                dca_schema = json.load(f)
            print("✅ DCA schema load successful")
        except Exception as e:
            print(f"❌ DCA schema load failed: {e}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Basic tests failed: {e}")
        return False


def generate_validation_report(results: Dict[str, bool]) -> None:
    """Générer un rapport de validation."""
    print("\n📊 Validation Report")
    print("=" * 50)
    
    total_checks = len(results)
    passed_checks = sum(1 for result in results.values() if result)
    success_rate = (passed_checks / total_checks) * 100
    
    print(f"Total checks: {total_checks}")
    print(f"Passed checks: {passed_checks}")
    print(f"Failed checks: {total_checks - passed_checks}")
    print(f"Success rate: {success_rate:.1f}%")
    
    print("\nDetailed results:")
    for check_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} {check_name}")
    
    if success_rate == 100:
        print("\n🎉 All validations passed! Migration is successful.")
    elif success_rate >= 80:
        print("\n⚠️  Most validations passed. Review failed checks.")
    else:
        print("\n❌ Many validations failed. Migration needs attention.")
    
    return success_rate


def main():
    """Fonction principale de validation."""
    
    print("🔍 Discovery Engine 2-Cat Migration Validation")
    print("=" * 60)
    
    # Vérifier qu'on est dans le bon répertoire
    if not Path("discovery-engine-2cat").exists():
        print("❌ Please run this script from the parent directory")
        return False
    
    # Changer vers le répertoire discovery-engine-2cat
    os.chdir("discovery-engine-2cat")
    
    # Exécuter toutes les vérifications
    results = {
        "Directory Structure": check_directory_structure(),
        "Orchestrator Components": check_orchestrator_components(),
        "Methods Components": check_methods_components(),
        "JSON Schemas": check_schemas(),
        "LLM Prompts": check_prompts(),
        "Scripts": check_scripts(),
        "Configuration Files": check_config_files(),
        "Import Statements": check_imports(),
        "Schema Validation": check_schema_validation(),
        "Domain Adapter": check_domain_adapter(),
        "Basic Tests": run_basic_tests()
    }
    
    # Générer le rapport
    success_rate = generate_validation_report(results)
    
    return success_rate >= 80


if __name__ == "__main__":
    success = main()
    if success:
        print("\n🚀 Migration validation completed successfully!")
        print("\nNext steps:")
        print("1. Configure the proof-engine-core submodule")
        print("2. Run: python scripts/setup_discovery_engine.py")
        print("3. Test: python scripts/test_discovery_engine.py")
        print("4. Demo: python scripts/demo_discovery_engine.py")
    else:
        print("\n🔧 Migration validation failed. Please review and fix issues.")
        exit(1)
