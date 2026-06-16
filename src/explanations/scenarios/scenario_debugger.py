"""Print full scenario objects for terminal debugging."""

from explanations.scenarios.models import FullScenario

def print_full_scenario(fs: FullScenario) -> None:
    """Write a FullScenario's probability, text, and notes to stdout."""
    print("=== Full Scenario ===")
    print(f"Probability : {fs.probability:.6f}")
    print("\nScenario:")
    print(fs.scenario)

    print("\nImplausible:")
    if fs.implausible:
        for item in fs.implausible:
            print(f"  - {item}")
    else:
        print("  None")

    print("\nSupporting:")
    if fs.supporting:
        for item in fs.supporting:
            print(f"  - {item}")
    else:
        print("  None")
        
        
# print("\n=== Scenario Explanation Debug ===")
#                 print(f"Target: {target}")
#                 print(f"Evidence: {evidence or {}}")
#                 print("Scope: direct parents of target + target")
#                 for scenario in scenarios:
#                     print(
#                         f"\nScenario {scenario['rank']} "
#                         f"(probability={scenario['probability']:.6f})"
#                     )
#                     for node, state in scenario["assignment"].items():
#                         print(f"  {node}: {state}")
#                     print(
#                         f"  Target outcome: {scenario['target']} = "
#                         f"{scenario['target_state']}"
#                     )
#                     print(
#                         f"  Target probability given scenario: "
#                         f"{scenario['target_probability']:.6f}"
#                     )
#                 print("=== End Scenario Explanation Debug ===\n")
#                 explain_content = dmc.Text(
#                     "Scenario debug output printed to the terminal."