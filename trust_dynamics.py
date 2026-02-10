"""
Trust Dynamics Module for Auracelle Bach
=========================================

Implements computational models of trust evolution, reciprocity, and reputation
in multi-agent AI governance simulations.

Based on:
- Ostrom, E. (1990). Governing the Commons
- Axelrod, R. (1984). The Evolution of Cooperation
- Fehr & Gächter (2000). Cooperation and Punishment
- Berg et al. (1995). Trust Game experiments
- Evans AGPO Framework trust formalization
"""

import numpy as np
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass, field
from enum import Enum
import json


class InteractionType(Enum):
    """Types of agent interactions that affect trust"""
    COOPERATION = "cooperation"
    DEFECTION = "defection"
    NEGOTIATION = "negotiation"
    ENFORCEMENT = "enforcement"
    INFORMATION_SHARING = "information_sharing"


class ReputationSignal(Enum):
    """Types of reputation information"""
    DIRECT_EXPERIENCE = "direct"      # First-hand interaction
    THIRD_PARTY = "third_party"       # Gossip/network information
    INSTITUTIONAL = "institutional"    # Formal ratings/enforcement
    PUBLIC_RECORD = "public"          # Observable actions


@dataclass
class InteractionRecord:
    """
    Record of a single interaction between agents
    Used for trust updating and reputation calculation
    """
    timestep: int
    agent_i: str  # Acting agent
    agent_j: str  # Target/partner agent
    interaction_type: InteractionType
    outcome_for_i: float  # Payoff/benefit for agent i [-1, 1]
    outcome_for_j: float  # Payoff/benefit for agent j [-1, 1]
    cooperation_level: float  # [0, 1] how cooperative was the action
    policy_context: Optional[str] = None  # Which policy was being negotiated


@dataclass
class TrustState:
    """
    Agent's trust beliefs about other agents in the network
    """
    agent_id: str

    # Trust network: trust level in each other agent [0, 1]
    trust_levels: Dict[str, float] = field(default_factory=dict)

    # Reputation beliefs: what agent thinks others' reputation is [0, 1]
    reputation_beliefs: Dict[str, float] = field(default_factory=dict)

    # Interaction history
    interaction_history: List[InteractionRecord] = field(default_factory=list)

    # Reciprocity tracking
    debts_owed: Dict[str, float] = field(default_factory=dict)  # Positive reciprocity
    grievances: Dict[str, float] = field(default_factory=dict)  # Negative reciprocity

    # Coalition/alliance memberships
    coalition_members: Set[str] = field(default_factory=set)

    # Trust characteristics
    baseline_trust: float = 0.5  # Initial trust in unknown agents
    trust_decay_rate: float = 0.02  # How fast trust erodes without interaction
    forgiveness_rate: float = 0.05  # How fast grievances fade
    reciprocity_strength: float = 0.7  # How much agent values reciprocity
    institutional_trust: float = 0.6  # Trust in governance mechanisms

    def get_trust(self, agent_j: str) -> float:
        """Get current trust level in agent j"""
        return self.trust_levels.get(agent_j, self.baseline_trust)

    def get_reputation_belief(self, agent_j: str) -> float:
        """Get believed reputation of agent j"""
        return self.reputation_beliefs.get(agent_j, 0.5)

    def get_net_reciprocity(self, agent_j: str) -> float:
        """
        Get net reciprocity balance with agent j
        Positive = they owe us, Negative = we owe them
        """
        debt = self.debts_owed.get(agent_j, 0.0)
        grievance = self.grievances.get(agent_j, 0.0)
        return debt - grievance


class TrustDynamicsEngine:
    """
    Core engine for trust evolution in governance networks
    """

    def __init__(self,
                 learning_rate: float = 0.3,
                 reputation_weight: float = 0.2,
                 institutional_weight: float = 0.15):
        """
        Initialize trust dynamics engine

        Args:
            learning_rate: How quickly trust updates from experience
            reputation_weight: How much third-party info influences trust
            institutional_weight: How much formal mechanisms affect trust
        """
        self.learning_rate = learning_rate
        self.reputation_weight = reputation_weight
        self.institutional_weight = institutional_weight

        # Network-level reputation scores
        self.global_reputation: Dict[str, float] = {}

        # Institutional enforcement probability
        self.enforcement_probability: float = 0.5

    def update_trust_from_interaction(self,
                                     agent_i_trust: TrustState,
                                     agent_j: str,
                                     interaction: InteractionRecord) -> float:
        """
        Update agent i's trust in agent j based on interaction outcome

        Implements Ostrom's trust evolution mechanism:
        Trust increases with cooperation, decreases with defection
        """
        current_trust = agent_i_trust.get_trust(agent_j)

        # Component 1: Direct experience update
        # Positive outcomes increase trust, negative decrease it
        outcome_signal = interaction.outcome_for_i

        # Trust update is asymmetric: losses hurt more than gains help
        if outcome_signal >= 0:
            experience_update = (
                outcome_signal *
                (1 - current_trust)  # Diminishing returns to trust building
            )
        else:
            # Betrayal is more damaging (loss aversion)
            experience_update = (
                outcome_signal * 1.5 *
                current_trust  # More to lose when trust is high
            )

        # Cooperation level modulates update
        cooperation_factor = interaction.cooperation_level
        weighted_experience = cooperation_factor * experience_update

        # Component 2: Reputation signal
        network_reputation = self.get_network_reputation(agent_j)
        reputation_signal = network_reputation - current_trust

        # Component 3: Institutional backing
        # If there are enforcement mechanisms, trust is more stable
        institutional_factor = (
            self.enforcement_probability *
            agent_i_trust.institutional_trust
        )

        # Combined trust update
        trust_change = (
            self.learning_rate * weighted_experience +
            self.reputation_weight * reputation_signal +
            self.institutional_weight * institutional_factor
        )

        new_trust = np.clip(current_trust + trust_change, 0, 1)

        # Update trust state
        agent_i_trust.trust_levels[agent_j] = new_trust

        # Record interaction
        agent_i_trust.interaction_history.append(interaction)

        return new_trust

    def update_reciprocity_accounts(self,
                                    agent_i_trust: TrustState,
                                    agent_j: str,
                                    interaction: InteractionRecord):
        """
        Update reciprocity debts and grievances
        Positive reciprocity: track who helped us
        Negative reciprocity: track who harmed us
        """
        outcome = interaction.outcome_for_i
        cooperation = interaction.cooperation_level

        # Positive reciprocity: agent j helped us
        if outcome > 0 and cooperation > 0.5:
            current_debt = agent_i_trust.debts_owed.get(agent_j, 0.0)
            # We now "owe" them for their help
            agent_i_trust.debts_owed[agent_j] = np.clip(
                current_debt + outcome * cooperation,
                0, 2.0  # Cap maximum debt
            )

        # Negative reciprocity: agent j harmed us
        if outcome < 0:
            current_grievance = agent_i_trust.grievances.get(agent_j, 0.0)
            # We now have a grievance to settle
            agent_i_trust.grievances[agent_j] = np.clip(
                current_grievance + abs(outcome),
                0, 2.0  # Cap maximum grievance
            )

    def compute_reciprocity_preference(self,
                                      agent_i_trust: TrustState,
                                      action_targets: List[str]) -> Dict[str, float]:
        """
        Compute reciprocity-based preference for cooperating with each target

        Returns preference scores [-1, 1] for each target agent
        """
        preferences = {}

        for agent_j in action_targets:
            # Positive reciprocity: prefer to help those who helped us
            debt = agent_i_trust.debts_owed.get(agent_j, 0.0)

            # Negative reciprocity: prefer to punish those who harmed us
            grievance = agent_i_trust.grievances.get(agent_j, 0.0)

            # Net preference
            reciprocity_preference = (
                agent_i_trust.reciprocity_strength *
                (debt - grievance)
            )

            preferences[agent_j] = np.clip(reciprocity_preference, -1, 1)

        return preferences

    def decay_trust_and_reciprocity(self, agent_trust: TrustState):
        """
        Apply time decay to trust levels and reciprocity accounts
        Trust erodes without positive interaction
        Reciprocity accounts fade over time (forgiveness)
        """
        # Trust decay
        for agent_j in agent_trust.trust_levels:
            current_trust = agent_trust.trust_levels[agent_j]

            # Trust decays toward baseline
            decay = agent_trust.trust_decay_rate * (current_trust - agent_trust.baseline_trust)
            agent_trust.trust_levels[agent_j] = np.clip(current_trust - decay, 0, 1)

        # Reciprocity decay (forgiveness)
        for agent_j in agent_trust.debts_owed:
            agent_trust.debts_owed[agent_j] *= (1 - agent_trust.forgiveness_rate)

        for agent_j in agent_trust.grievances:
            agent_trust.grievances[agent_j] *= (1 - agent_trust.forgiveness_rate)

    def update_network_reputation(self,
                                  agent_id: str,
                                  all_interactions: List[InteractionRecord]):
        """
        Update global network reputation based on all visible interactions
        Reputation = average cooperation/fairness across all interactions
        """
        relevant_interactions = [
            interaction for interaction in all_interactions
            if interaction.agent_i == agent_id or interaction.agent_j == agent_id
        ]

        if not relevant_interactions:
            self.global_reputation[agent_id] = 0.5  # Neutral
            return

        # Compute average cooperation as reputation proxy
        cooperation_scores = []
        for interaction in relevant_interactions:
            if interaction.agent_i == agent_id:
                # Agent's cooperation in this interaction
                cooperation_scores.append(interaction.cooperation_level)
            else:
                # If agent_j, infer cooperation from outcome
                if interaction.outcome_for_j > 0:
                    cooperation_scores.append(0.7)
                elif interaction.outcome_for_j < 0:
                    cooperation_scores.append(0.3)
                else:
                    cooperation_scores.append(0.5)

        reputation = np.mean(cooperation_scores)

        # Update with exponential smoothing
        old_reputation = self.global_reputation.get(agent_id, 0.5)
        self.global_reputation[agent_id] = 0.7 * old_reputation + 0.3 * reputation

    def get_network_reputation(self, agent_id: str) -> float:
        """Get agent's network-wide reputation [0, 1]"""
        return self.global_reputation.get(agent_id, 0.5)

    def compute_trust_based_cooperation_incentive(self,
                                                  agent_i_trust: TrustState,
                                                  agent_j: str) -> float:
        """
        Compute how much trust incentivizes cooperation with agent j

        High trust → willing to cooperate even without immediate payoff
        Low trust → require strong incentives to cooperate

        Returns cooperation bonus [-0.5, 0.5]
        """
        trust_level = agent_i_trust.get_trust(agent_j)

        # Trust provides cooperation bonus
        # Trust=1 gives max bonus, Trust=0 gives penalty
        cooperation_bonus = (trust_level - 0.5)

        # Modulated by reciprocity balance
        reciprocity = agent_i_trust.get_net_reciprocity(agent_j)

        total_incentive = cooperation_bonus + 0.3 * reciprocity

        return np.clip(total_incentive, -0.5, 0.5)


class CoalitionManager:
    """
    Manages coalition formation based on trust and value alignment
    """

    def __init__(self,
                 trust_threshold: float = 0.6,
                 value_alignment_weight: float = 0.4):
        """
        Args:
            trust_threshold: Minimum trust needed to form coalition
            value_alignment_weight: How much moral alignment matters vs trust
        """
        self.trust_threshold = trust_threshold
        self.value_alignment_weight = value_alignment_weight

        # Active coalitions
        self.coalitions: Dict[str, Set[str]] = {}  # coalition_id -> member set

    def can_form_coalition(self,
                          agent_i_trust: TrustState,
                          agent_j: str,
                          moral_distance: Optional[float] = None) -> bool:
        """
        Determine if two agents can form a coalition
        Requires sufficient trust and value alignment
        """
        trust = agent_i_trust.get_trust(agent_j)

        # Check trust threshold
        if trust < self.trust_threshold:
            return False

        # Check value alignment if provided
        if moral_distance is not None:
            # moral_distance [0, ~1.4], lower is better
            alignment_score = 1 - (moral_distance / 1.5)

            combined_score = (
                (1 - self.value_alignment_weight) * trust +
                self.value_alignment_weight * alignment_score
            )

            return combined_score > 0.65

        return True

    def form_coalition(self,
                      coalition_id: str,
                      members: Set[str]):
        """Create a new coalition"""
        self.coalitions[coalition_id] = members

    def update_coalition_trust(self,
                              coalition_id: str,
                              member_trust_states: Dict[str, TrustState]):
        """
        Update in-coalition trust bonuses
        Coalition members get trust boost toward each other
        """
        if coalition_id not in self.coalitions:
            return

        members = self.coalitions[coalition_id]
        coalition_trust_bonus = 0.1

        for agent_i in members:
            if agent_i not in member_trust_states:
                continue

            trust_state = member_trust_states[agent_i]

            for agent_j in members:
                if agent_i != agent_j:
                    current_trust = trust_state.get_trust(agent_j)
                    # Coalition membership boosts trust
                    trust_state.trust_levels[agent_j] = np.clip(
                        current_trust + coalition_trust_bonus,
                        0, 1
                    )
                    # Update coalition membership
                    trust_state.coalition_members.add(agent_j)


class TrustBasedPolicyNegotiation:
    """
    Models how trust affects policy negotiation dynamics
    """

    def __init__(self, trust_engine: TrustDynamicsEngine):
        self.trust_engine = trust_engine

    def compute_negotiation_power(self,
                                  agent_trust: TrustState,
                                  other_agents: List[str]) -> float:
        """
        Compute agent's negotiation power based on network trust
        High trust = more influence in negotiations
        """
        # Average trust others have in this agent (reputation)
        reputation = self.trust_engine.get_network_reputation(agent_trust.agent_id)

        # Agent's own trust in others (willingness to cooperate)
        own_trust = np.mean([
            agent_trust.get_trust(other)
            for other in other_agents
        ])

        # Coalition size bonus
        coalition_bonus = 0.1 * len(agent_trust.coalition_members)

        negotiation_power = (
            0.5 * reputation +
            0.3 * own_trust +
            0.2 * coalition_bonus
        )

        return np.clip(negotiation_power, 0, 1)

    def compute_compromise_willingness(self,
                                      agent_i_trust: TrustState,
                                      agent_j: str,
                                      policy_value_gap: float) -> float:
        """
        How willing is agent i to compromise with agent j?

        High trust → willing to accept suboptimal deals
        Low trust → demand better terms

        Args:
            policy_value_gap: How much policy differs from agent's ideal [-1, 1]

        Returns:
            Compromise willingness [0, 1]
        """
        trust = agent_i_trust.get_trust(agent_j)
        reciprocity = agent_i_trust.get_net_reciprocity(agent_j)

        # Base willingness from trust
        base_willingness = trust

        # Reciprocity adjustment
        if reciprocity > 0:
            # They helped us before, more willing to compromise
            willingness = base_willingness + 0.2 * reciprocity
        elif reciprocity < 0:
            # We have grievance, less willing
            willingness = base_willingness + 0.3 * reciprocity  # Negative impact
        else:
            willingness = base_willingness

        # Modulated by policy value gap
        # Small gaps → easier to compromise even with low trust
        gap_factor = 1 - abs(policy_value_gap)

        final_willingness = willingness * (0.5 + 0.5 * gap_factor)

        return np.clip(final_willingness, 0, 1)

    def model_repeated_game_strategy(self,
                                    agent_i_trust: TrustState,
                                    agent_j: str,
                                    history_length: int = 5) -> str:
        """
        Determine cooperation strategy based on trust and history
        Implements variants of Tit-for-Tat

        Returns: "cooperate", "defect", "conditional_cooperate"
        """
        trust = agent_i_trust.get_trust(agent_j)

        # Get recent interaction history
        recent_interactions = [
            interaction for interaction in agent_i_trust.interaction_history[-history_length:]
            if interaction.agent_j == agent_j
        ]

        if not recent_interactions:
            # No history: trust-based decision
            return "cooperate" if trust > 0.6 else "conditional_cooperate"

        # Check if agent j cooperated recently
        recent_cooperation = np.mean([
            interaction.cooperation_level
            for interaction in recent_interactions
        ])

        # Tit-for-Tat with forgiveness
        if recent_cooperation > 0.7:
            return "cooperate"  # They cooperated, reciprocate
        elif recent_cooperation < 0.3:
            # They defected
            grievance = agent_i_trust.grievances.get(agent_j, 0.0)
            if grievance > 1.0 and trust < 0.3:
                return "defect"  # Punish severe betrayal
            else:
                return "conditional_cooperate"  # Forgive but cautious
        else:
            # Mixed signals
            return "conditional_cooperate" if trust > 0.5 else "defect"


# ============================================================================
# TRUST-BASED GOVERNANCE SCENARIOS
# ============================================================================

def create_governance_network_trust_states(agent_ids: List[str]) -> Dict[str, TrustState]:
    """
    Initialize trust states for all agents in governance network
    """
    trust_states = {}

    for agent_id in agent_ids:
        trust_states[agent_id] = TrustState(
            agent_id=agent_id,
            baseline_trust=0.5,
            trust_decay_rate=0.02,
            forgiveness_rate=0.05,
            reciprocity_strength=0.7,
            institutional_trust=0.6
        )

    return trust_states


def simulate_trust_evolution_example():
    """
    Demonstrate trust dynamics in AI governance negotiation
    """
    print("=" * 80)
    print("TRUST DYNAMICS MODULE - VALIDATION EXAMPLE")
    print("=" * 80)
    print()

    # Create agents
    agents = ["Government_A", "TechCorp", "ConsumerNGO", "StandardsBody"]
    trust_states = create_governance_network_trust_states(agents)

    # Initialize trust engine
    engine = TrustDynamicsEngine(
        learning_rate=0.3,
        reputation_weight=0.2,
        institutional_weight=0.15
    )

    # Initialize coalition manager
    coalition_mgr = CoalitionManager(trust_threshold=0.6)

    print("INITIAL STATE:")
    print("-" * 80)
    for agent_id in agents:
        print(f"{agent_id}: Baseline trust = {trust_states[agent_id].baseline_trust}")
    print()

    # Simulate negotiation rounds
    print("\nNEGOTIATION ROUND 1: Data Privacy Policy")
    print("-" * 80)

    # Interaction 1: TechCorp cooperates with Government_A
    interaction1 = InteractionRecord(
        timestep=1,
        agent_i="TechCorp",
        agent_j="Government_A",
        interaction_type=InteractionType.NEGOTIATION,
        outcome_for_i=0.6,  # Moderate gain for TechCorp
        outcome_for_j=0.7,  # Good outcome for Government
        cooperation_level=0.8,  # High cooperation
        policy_context="data_privacy"
    )

    new_trust = engine.update_trust_from_interaction(
        trust_states["TechCorp"],
        "Government_A",
        interaction1
    )
    engine.update_reciprocity_accounts(
        trust_states["TechCorp"],
        "Government_A",
        interaction1
    )

    print(f"TechCorp cooperates with Government_A (cooperation=0.8)")
    print(f"  → TechCorp's trust in Government_A: {trust_states['TechCorp'].baseline_trust:.2f} → {new_trust:.2f}")
    print(f"  → Reciprocity debt owed to Government_A: {trust_states['TechCorp'].debts_owed.get('Government_A', 0):.2f}")
    print()

    # Interaction 2: ConsumerNGO defects against TechCorp
    interaction2 = InteractionRecord(
        timestep=1,
        agent_i="ConsumerNGO",
        agent_j="TechCorp",
        interaction_type=InteractionType.NEGOTIATION,
        outcome_for_i=0.4,
        outcome_for_j=-0.5,  # Negative outcome for TechCorp
        cooperation_level=0.2,  # Low cooperation (defection)
        policy_context="data_privacy"
    )

    new_trust = engine.update_trust_from_interaction(
        trust_states["ConsumerNGO"],
        "TechCorp",
        interaction2
    )
    engine.update_reciprocity_accounts(
        trust_states["ConsumerNGO"],
        "TechCorp",
        interaction2
    )

    print(f"ConsumerNGO defects against TechCorp (cooperation=0.2)")
    print(f"  → ConsumerNGO's trust in TechCorp: {trust_states['ConsumerNGO'].baseline_trust:.2f} → {new_trust:.2f}")
    print()

    # Update TechCorp's trust in ConsumerNGO (perspective flip)
    interaction2_reverse = InteractionRecord(
        timestep=1,
        agent_i="TechCorp",
        agent_j="ConsumerNGO",
        interaction_type=InteractionType.NEGOTIATION,
        outcome_for_i=-0.5,
        outcome_for_j=0.4,
        cooperation_level=0.2,
        policy_context="data_privacy"
    )

    new_trust_reverse = engine.update_trust_from_interaction(
        trust_states["TechCorp"],
        "ConsumerNGO",
        interaction2_reverse
    )
    engine.update_reciprocity_accounts(
        trust_states["TechCorp"],
        "ConsumerNGO",
        interaction2_reverse
    )

    print(f"TechCorp experiences defection from ConsumerNGO")
    print(f"  → TechCorp's trust in ConsumerNGO: {trust_states['TechCorp'].baseline_trust:.2f} → {new_trust_reverse:.2f}")
    print(f"  → Grievance against ConsumerNGO: {trust_states['TechCorp'].grievances.get('ConsumerNGO', 0):.2f}")
    print()

    # Update network reputations
    all_interactions = [interaction1, interaction2, interaction2_reverse]
    for agent_id in agents:
        engine.update_network_reputation(agent_id, all_interactions)

    print("\nNETWORK REPUTATION SCORES:")
    print("-" * 80)
    for agent_id in agents:
        reputation = engine.get_network_reputation(agent_id)
        print(f"{agent_id}: {reputation:.2f}")
    print()

    # Coalition formation
    print("\nCOALITION FORMATION:")
    print("-" * 80)

    can_coalition = coalition_mgr.can_form_coalition(
        trust_states["TechCorp"],
        "Government_A",
        moral_distance=0.3  # Moderate value alignment
    )

    print(f"Can TechCorp form coalition with Government_A? {can_coalition}")
    print(f"  (Trust: {trust_states['TechCorp'].get_trust('Government_A'):.2f}, "
          f"Threshold: {coalition_mgr.trust_threshold})")

    if can_coalition:
        coalition_mgr.form_coalition("tech_gov_alliance", {"TechCorp", "Government_A"})
        print("  → Coalition 'tech_gov_alliance' formed!")
    print()

    # Negotiation dynamics
    print("\nNEGOTIATION ROUND 2: AI Safety Standards")
    print("-" * 80)

    negotiator = TrustBasedPolicyNegotiation(engine)

    # Compute negotiation power
    for agent_id in agents:
        power = negotiator.compute_negotiation_power(
            trust_states[agent_id],
            [a for a in agents if a != agent_id]
        )
        print(f"{agent_id} negotiation power: {power:.2f}")
    print()

    # Compute compromise willingness
    print("\nCOMPROMISE WILLINGNESS:")
    print("-" * 80)

    # TechCorp willing to compromise with Government_A (high trust)
    willingness_high_trust = negotiator.compute_compromise_willingness(
        trust_states["TechCorp"],
        "Government_A",
        policy_value_gap=0.3  # Moderate disagreement
    )

    # TechCorp unwilling to compromise with ConsumerNGO (low trust, grievance)
    willingness_low_trust = negotiator.compute_compromise_willingness(
        trust_states["TechCorp"],
        "ConsumerNGO",
        policy_value_gap=0.3
    )

    print(f"TechCorp → Government_A: {willingness_high_trust:.2f} (high trust)")
    print(f"TechCorp → ConsumerNGO: {willingness_low_trust:.2f} (low trust, grievance)")
    print()

    # Repeated game strategies
    print("\nREPEATED GAME STRATEGIES:")
    print("-" * 80)

    strategy_gov = negotiator.model_repeated_game_strategy(
        trust_states["TechCorp"],
        "Government_A"
    )

    strategy_ngo = negotiator.model_repeated_game_strategy(
        trust_states["TechCorp"],
        "ConsumerNGO"
    )

    print(f"TechCorp strategy toward Government_A: {strategy_gov}")
    print(f"TechCorp strategy toward ConsumerNGO: {strategy_ngo}")
    print()

    # Trust decay over time
    print("\nTIME DECAY (10 rounds without interaction):")
    print("-" * 80)

    for timestep in range(10):
        engine.decay_trust_and_reciprocity(trust_states["TechCorp"])

    print(f"TechCorp's trust in Government_A after decay: "
          f"{trust_states['TechCorp'].get_trust('Government_A'):.2f}")
    print(f"Reciprocity debt after decay: "
          f"{trust_states['TechCorp'].debts_owed.get('Government_A', 0):.2f}")
    print(f"Grievance against ConsumerNGO after decay: "
          f"{trust_states['TechCorp'].grievances.get('ConsumerNGO', 0):.2f}")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    simulate_trust_evolution_example()
