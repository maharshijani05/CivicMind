import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ui.simulation_engine import run_simulation

policy = "A new ₹100 congestion tax will apply to all vehicles entering the city center on weekdays."

results = run_simulation(policy)

print("\n🔷 CitizenBot:\n", results["citizen"])
print("\n🔷 BusinessBot:\n", results["business"])
print("\n🔷 PoliticianBot:\n", results["politician"])
print("\n🔷 ActivistBot:\n", results["activist"])
print("\n📰 JournalistBot Summary:\n", results["journalist"])
