"""
Moral Foundations Module for Auracelle Bach
============================================

Implements Haidt's Moral Foundations Theory for AI governance policy evaluation.
Provides computational framework for value-weighted decision-making in multi-agent
governance simulations.

Based on:
- Haidt, J. (2012). The Righteous Mind
- Graham et al. (2013). Moral Foundations Theory
- Evans AGPO Framework mathematical formalization
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum
import json


class FoundationType(Enum):
    """Five moral foundations from Haidt's theory"""
    CARE_HARM = "care_harm"
    FAIRNESS_CHEATING = "fairness_cheating"
    LOYALTY_BETRAYAL = "loyalty_betrayal"
    AUTHORITY_SUBVERSION = "authority_subversion"
    SANCTITY_DEGRADATION = "sanctity_degradation"


@dataclass
class PolicyFeatures:
    """
    Structured representation of AI governance policy characteristics
    for moral evaluation
    """
    # Core policy attributes
    policy_id: str
    policy_name: str
    policy_type: str  # 'regulation', 'standard', 'mandate', 'incentive'

    # Care/Harm dimensions
    safety_requirements: float = 0.5  # [0,1] strength of safety provisions
    harm_prevention: float = 0.5      # [0,1] explicit harm mitigation
    vulnerable_protection: float = 0.5 # [0,1] protections for vulnerable groups
    privacy_safeguards: float = 0.5   # [0,1] privacy protection level

    # Fairness dimensions
    equity_provisions: float = 0.5     # [0,1] distributional fairness
    procedural_fairness: float = 0.5   # [0,1] transparent/accountable process
    access_equality: float = 0.5       # [0,1] equal access to benefits
    small_actor_burden: float = 0.5    # [0,1] disproportionate impact on small players

    # Loyalty dimensions
    national_advantage: float = 0.5    # [0,1] benefit to domestic industry
    competitiveness_impact: float = 0.5 # [0,1] effect on international position
    cross_border_cooperation: float = 0.5 # [0,1] promotes international alignment
    ingroup_solidarity: float = 0.5    # [0,1] strengthens community bonds

    # Authority dimensions
    institutional_clarity: float = 0.5  # [0,1] clear governance structure
    regulatory_strength: float = 0.5    # [0,1] enforcement capability
    precedent_alignment: float = 0.5    # [0,1] consistency with existing law
    expert_deference: float = 0.5       # [0,1] respects technical expertise

    # Sanctity dimensions
    human_dignity: float = 0.5          # [0,1] preserves human autonomy
    privacy_sanctity: float = 0.5       # [0,1] treats privacy as inviolable
    transparency_norms: float = 0.5     # [0,1] upholds democratic values
    manipulation_prevention: float = 0.5 # [0,1] prevents behavioral exploitation

    # Meta-attributes
    implementation_cost: float = 0.5    # [0,1] economic burden
    innovation_impact: float = 0.5      # [0,1] effect on AI development
    enforcement_difficulty: float = 0.5 # [0,1] practical implementability


@dataclass
class MoralFoundations:
    """
    Agent's moral foundation weights
    Determines how strongly each moral dimension influences decision-making
    """
    care_harm: float = 0.2            # Weight on preventing suffering
    fairness_cheating: float = 0.2    # Weight on justice/equity
    loyalty_betrayal: float = 0.2     # Weight on group solidarity
    authority_subversion: float = 0.2 # Weight on institutional order
    sanctity_degradation: float = 0.2 # Weight on human dignity/purity

    def __post_init__(self):
        """Normalize weights to sum to 1.0"""
        total = (self.care_harm + self.fairness_cheating +
                self.loyalty_betrayal + self.authority_subversion +
                self.sanctity_degradation)
        if total > 0:
            self.care_harm /= total
            self.fairness_cheating /= total
            self.loyalty_betrayal /= total
            self.authority_subversion /= total
            self.sanctity_degradation /= total

    def to_dict(self) -> Dict[str, float]:
        """Convert to dictionary for serialization"""
        return {
            'care_harm': self.care_harm,
            'fairness_cheating': self.fairness_cheating,
            'loyalty_betrayal': self.loyalty_betrayal,
            'authority_subversion': self.authority_subversion,
            'sanctity_degradation': self.sanctity_degradation
        }

    def distance_to(self, other: 'MoralFoundations') -> float:
        """
        Compute moral distance between two foundation profiles
        Used for modeling value similarity between agents
        """
        return np.sqrt(
            (self.care_harm - other.care_harm) ** 2 +
            (self.fairness_cheating - other.fairness_cheating) ** 2 +
            (self.loyalty_betrayal - other.loyalty_betrayal) ** 2 +
            (self.authority_subversion - other.authority_subversion) ** 2 +
            (self.sanctity_degradation - other.sanctity_degradation) ** 2
        )


class MoralEvaluator:
    """
    Core moral evaluation engine
    Computes moral valence of policies across all five foundations
    """

    def __init__(self, scenario_context: str = "general"):
        """
        Initialize evaluator with scenario-specific calibration

        Args:
            scenario_context: 'data_privacy', 'ethics_board', 'transparency', 'general'
        """
        self.scenario_context = scenario_context
        self.harm_weights = self._initialize_harm_weights()
        self.fairness_weights = self._initialize_fairness_weights()
        self.loyalty_weights = self._initialize_loyalty_weights()
        self.authority_weights = self._initialize_authority_weights()
        self.sanctity_weights = self._initialize_sanctity_weights()

    def _initialize_harm_weights(self) -> Dict[str, float]:
        """Scenario-specific weights for harm evaluation"""
        base_weights = {
            'safety': 0.30,
            'privacy': 0.25,
            'vulnerable_protection': 0.25,
            'harm_prevention': 0.20
        }

        # Adjust for scenario
        if self.scenario_context == "data_privacy":
            base_weights['privacy'] = 0.40
            base_weights['safety'] = 0.20
        elif self.scenario_context == "ethics_board":
            base_weights['vulnerable_protection'] = 0.35
            base_weights['harm_prevention'] = 0.30

        return base_weights

    def _initialize_fairness_weights(self) -> Dict[str, float]:
        """Scenario-specific weights for fairness evaluation"""
        base_weights = {
            'equity': 0.30,
            'procedural': 0.30,
            'access': 0.25,
            'burden_distribution': 0.15
        }

        if self.scenario_context == "ethics_board":
            base_weights['procedural'] = 0.40
            base_weights['equity'] = 0.35
        elif self.scenario_context == "transparency":
            base_weights['procedural'] = 0.45
            base_weights['access'] = 0.30

        return base_weights

    def _initialize_loyalty_weights(self) -> Dict[str, float]:
        """Scenario-specific weights for loyalty evaluation"""
        return {
            'national_interest': 0.35,
            'competitiveness': 0.30,
            'cooperation': 0.20,
            'solidarity': 0.15
        }

    def _initialize_authority_weights(self) -> Dict[str, float]:
        """Scenario-specific weights for authority evaluation"""
        return {
            'institutional_clarity': 0.30,
            'enforcement': 0.25,
            'precedent': 0.25,
            'expertise': 0.20
        }

    def _initialize_sanctity_weights(self) -> Dict[str, float]:
        """Scenario-specific weights for sanctity evaluation"""
        base_weights = {
            'human_dignity': 0.35,
            'privacy_sanctity': 0.30,
            'transparency_norms': 0.20,
            'manipulation_prevention': 0.15
        }

        if self.scenario_context == "data_privacy":
            base_weights['privacy_sanctity'] = 0.45
            base_weights['human_dignity'] = 0.30

        return base_weights

    def evaluate_care_harm(self, policy: PolicyFeatures) -> float:
        """
        Evaluate policy on Care/Harm foundation

        Higher scores = more protective of wellbeing, less harmful
        Range: [-1, 1]
        """
        # Positive contributions (care)
        care_score = (
            self.harm_weights['safety'] * policy.safety_requirements +
            self.harm_weights['privacy'] * policy.privacy_safeguards +
            self.harm_weights['vulnerable_protection'] * policy.vulnerable_protection +
            self.harm_weights['harm_prevention'] * policy.harm_prevention
        )

        # Negative contributions (potential harms from regulation itself)
        regulatory_harm = (
            0.3 * policy.implementation_cost +  # Economic harm
            0.2 * policy.enforcement_difficulty  # Compliance burden
        )

        net_score = care_score - 0.3 * regulatory_harm

        return np.clip(2 * net_score - 1, -1, 1)  # Normalize to [-1, 1]

    def evaluate_fairness_cheating(self, policy: PolicyFeatures) -> float:
        """
        Evaluate policy on Fairness/Cheating foundation

        Higher scores = more fair, equitable, just
        Range: [-1, 1]
        """
        # Positive contributions (fairness)
        fairness_score = (
            self.fairness_weights['equity'] * policy.equity_provisions +
            self.fairness_weights['procedural'] * policy.procedural_fairness +
            self.fairness_weights['access'] * policy.access_equality
        )

        # Negative contributions (unfairness)
        unfairness_penalty = (
            self.fairness_weights['burden_distribution'] *
            policy.small_actor_burden  # Disproportionate burden is unfair
        )

        net_score = fairness_score - unfairness_penalty

        return np.clip(2 * net_score - 1, -1, 1)

    def evaluate_loyalty_betrayal(self, policy: PolicyFeatures) -> float:
        """
        Evaluate policy on Loyalty/Betrayal foundation

        Higher scores = strengthens ingroup, protects national interests
        Range: [-1, 1]
        """
        loyalty_score = (
            self.loyalty_weights['national_interest'] * policy.national_advantage +
            self.loyalty_weights['competitiveness'] * (1 - policy.competitiveness_impact) +
            self.loyalty_weights['cooperation'] * policy.cross_border_cooperation +
            self.loyalty_weights['solidarity'] * policy.ingroup_solidarity
        )

        # Note: competitiveness_impact represents harm to competitiveness, so we invert it

        return np.clip(2 * loyalty_score - 1, -1, 1)

    def evaluate_authority_subversion(self, policy: PolicyFeatures) -> float:
        """
        Evaluate policy on Authority/Subversion foundation

        Higher scores = strengthens legitimate authority, clear governance
        Range: [-1, 1]
        """
        authority_score = (
            self.authority_weights['institutional_clarity'] * policy.institutional_clarity +
            self.authority_weights['enforcement'] * policy.regulatory_strength +
            self.authority_weights['precedent'] * policy.precedent_alignment +
            self.authority_weights['expertise'] * policy.expert_deference
        )

        return np.clip(2 * authority_score - 1, -1, 1)

    def evaluate_sanctity_degradation(self, policy: PolicyFeatures) -> float:
        """
        Evaluate policy on Sanctity/Degradation foundation

        Higher scores = protects human dignity, prevents degradation
        Range: [-1, 1]
        """
        sanctity_score = (
            self.sanctity_weights['human_dignity'] * policy.human_dignity +
            self.sanctity_weights['privacy_sanctity'] * policy.privacy_sanctity +
            self.sanctity_weights['transparency_norms'] * policy.transparency_norms +
            self.sanctity_weights['manipulation_prevention'] * policy.manipulation_prevention
        )

        return np.clip(2 * sanctity_score - 1, -1, 1)

    def evaluate_all_foundations(self, policy: PolicyFeatures) -> Dict[str, float]:
        """
        Compute moral evaluation across all five foundations

        Returns:
            Dictionary mapping foundation names to scores [-1, 1]
        """
        return {
            'care_harm': self.evaluate_care_harm(policy),
            'fairness_cheating': self.evaluate_fairness_cheating(policy),
            'loyalty_betrayal': self.evaluate_loyalty_betrayal(policy),
            'authority_subversion': self.evaluate_authority_subversion(policy),
            'sanctity_degradation': self.evaluate_sanctity_degradation(policy)
        }

    def compute_moral_value(self,
                           policy: PolicyFeatures,
                           agent_foundations: MoralFoundations) -> float:
        """
        Compute overall moral value of policy for agent with specific foundation weights

        This is the key function for value-weighted decision-making

        Args:
            policy: Policy to evaluate
            agent_foundations: Agent's moral foundation weights

        Returns:
            Weighted moral value [-1, 1]
        """
        foundation_scores = self.evaluate_all_foundations(policy)

        moral_value = (
            agent_foundations.care_harm * foundation_scores['care_harm'] +
            agent_foundations.fairness_cheating * foundation_scores['fairness_cheating'] +
            agent_foundations.loyalty_betrayal * foundation_scores['loyalty_betrayal'] +
            agent_foundations.authority_subversion * foundation_scores['authority_subversion'] +
            agent_foundations.sanctity_degradation * foundation_scores['sanctity_degradation']
        )

        return moral_value

    def check_moral_constraints(self,
                                policy: PolicyFeatures,
                                agent_foundations: MoralFoundations,
                                threshold: float = -0.5) -> Tuple[bool, List[str]]:
        """
        Check if policy violates any moral hard constraints

        Some agents may have deontological rules: certain foundations
        must not fall below threshold (inadmissible actions)

        Args:
            policy: Policy to check
            agent_foundations: Agent's moral weights
            threshold: Minimum acceptable score for any strongly-weighted foundation

        Returns:
            (is_admissible, list_of_violations)
        """
        foundation_scores = self.evaluate_all_foundations(policy)
        violations = []

        # Check if any strongly-weighted foundation is severely violated
        for foundation_name, score in foundation_scores.items():
            weight = getattr(agent_foundations, foundation_name)

            # If agent weights this foundation highly (>0.25) and score is very negative
            if weight > 0.25 and score < threshold:
                violations.append(f"{foundation_name}: {score:.2f} (threshold: {threshold})")

        is_admissible = len(violations) == 0
        return is_admissible, violations


class MoralExplainer:
    """
    Generate human-readable explanations of moral evaluations
    Crucial for interpretability in Cambridge research validation
    """

    def __init__(self, evaluator: MoralEvaluator):
        self.evaluator = evaluator

    def explain_evaluation(self,
                          policy: PolicyFeatures,
                          agent_foundations: MoralFoundations,
                          agent_name: str = "Agent") -> str:
        """
        Generate natural language explanation of why agent supports/opposes policy
        """
        foundation_scores = self.evaluator.evaluate_all_foundations(policy)
        moral_value = self.evaluator.compute_moral_value(policy, agent_foundations)

        # Determine overall stance
        if moral_value > 0.3:
            stance = "strongly supports"
        elif moral_value > 0:
            stance = "supports"
        elif moral_value > -0.3:
            stance = "opposes"
        else:
            stance = "strongly opposes"

        # Identify dominant foundation
        weighted_scores = {
            name: getattr(agent_foundations, name) * score
            for name, score in foundation_scores.items()
        }
        dominant_foundation = max(weighted_scores, key=weighted_scores.get)
        dominant_value = weighted_scores[dominant_foundation]

        # Generate explanation
        explanation = f"""
{agent_name} {stance} "{policy.policy_name}" (Overall Moral Value: {moral_value:.2f})

PRIMARY MORAL REASONING:
{self._explain_foundation(dominant_foundation, foundation_scores[dominant_foundation], policy)}

FOUNDATION BREAKDOWN:
"""

        for foundation_name, score in foundation_scores.items():
            weight = getattr(agent_foundations, foundation_name)
            contribution = weight * score
            explanation += f"  • {foundation_name.replace('_', '/').title()}: "
            explanation += f"{score:+.2f} (weight: {weight:.2f}, contribution: {contribution:+.2f})\n"

        # Identify moral conflicts
        conflicts = self._identify_conflicts(foundation_scores, agent_foundations)
        if conflicts:
            explanation += "\nMORAL TENSIONS:\n"
            for conflict in conflicts:
                explanation += f"  • {conflict}\n"

        return explanation

    def _explain_foundation(self, foundation: str, score: float, policy: PolicyFeatures) -> str:
        """Generate foundation-specific explanation"""

        explanations = {
            'care_harm': self._explain_care_harm(score, policy),
            'fairness_cheating': self._explain_fairness(score, policy),
            'loyalty_betrayal': self._explain_loyalty(score, policy),
            'authority_subversion': self._explain_authority(score, policy),
            'sanctity_degradation': self._explain_sanctity(score, policy)
        }

        return explanations.get(foundation, "No explanation available")

    def _explain_care_harm(self, score: float, policy: PolicyFeatures) -> str:
        if score > 0:
            return (f"This policy effectively protects people from harm "
                   f"(safety: {policy.safety_requirements:.2f}, "
                   f"privacy: {policy.privacy_safeguards:.2f}, "
                   f"vulnerable groups: {policy.vulnerable_protection:.2f})")
        else:
            return (f"This policy may cause harm through regulatory burden "
                   f"or insufficient protection "
                   f"(implementation cost: {policy.implementation_cost:.2f})")

    def _explain_fairness(self, score: float, policy: PolicyFeatures) -> str:
        if score > 0:
            return (f"This policy promotes fairness and equity "
                   f"(equity provisions: {policy.equity_provisions:.2f}, "
                   f"procedural fairness: {policy.procedural_fairness:.2f})")
        else:
            return (f"This policy creates unfair burdens "
                   f"(small actor burden: {policy.small_actor_burden:.2f}, "
                   f"access inequality: {1-policy.access_equality:.2f})")

    def _explain_loyalty(self, score: float, policy: PolicyFeatures) -> str:
        if score > 0:
            return (f"This policy serves national/group interests "
                   f"(national advantage: {policy.national_advantage:.2f}, "
                   f"cooperation: {policy.cross_border_cooperation:.2f})")
        else:
            return (f"This policy may harm competitiveness or group solidarity "
                   f"(competitiveness impact: {policy.competitiveness_impact:.2f})")

    def _explain_authority(self, score: float, policy: PolicyFeatures) -> str:
        if score > 0:
            return (f"This policy strengthens institutional governance "
                   f"(institutional clarity: {policy.institutional_clarity:.2f}, "
                   f"regulatory strength: {policy.regulatory_strength:.2f})")
        else:
            return (f"This policy weakens governance structures or precedent "
                   f"(precedent alignment: {policy.precedent_alignment:.2f})")

    def _explain_sanctity(self, score: float, policy: PolicyFeatures) -> str:
        if score > 0:
            return (f"This policy protects human dignity and autonomy "
                   f"(human dignity: {policy.human_dignity:.2f}, "
                   f"manipulation prevention: {policy.manipulation_prevention:.2f})")
        else:
            return (f"This policy may compromise dignity or sacred values "
                   f"(privacy sanctity: {policy.privacy_sanctity:.2f})")

    def _identify_conflicts(self,
                           foundation_scores: Dict[str, float],
                           agent_foundations: MoralFoundations) -> List[str]:
        """Identify moral tradeoffs where foundations conflict"""
        conflicts = []

        weighted = {k: getattr(agent_foundations, k) * v
                   for k, v in foundation_scores.items()}

        # Find foundations with significant weight that conflict
        for f1, score1 in weighted.items():
            for f2, score2 in weighted.items():
                if f1 < f2:  # Avoid duplicates
                    # If both weighted significantly but opposite signs
                    if abs(score1) > 0.1 and abs(score2) > 0.1:
                        if np.sign(score1) != np.sign(score2):
                            conflicts.append(
                                f"{f1.replace('_', '/').title()} ({score1:+.2f}) "
                                f"conflicts with {f2.replace('_', '/').title()} ({score2:+.2f})"
                            )

        return conflicts


# ============================================================================
# STAKEHOLDER MORAL PROFILES
# ============================================================================

STAKEHOLDER_PROFILES = {
    "consumer_advocacy_ngo": MoralFoundations(
        care_harm=0.45,
        fairness_cheating=0.35,
        loyalty_betrayal=0.05,
        authority_subversion=0.10,
        sanctity_degradation=0.05
    ),

    "tech_industry_association": MoralFoundations(
        care_harm=0.20,
        fairness_cheating=0.25,
        loyalty_betrayal=0.15,
        authority_subversion=0.30,
        sanctity_degradation=0.10
    ),

    "progressive_government": MoralFoundations(
        care_harm=0.35,
        fairness_cheating=0.30,
        loyalty_betrayal=0.10,
        authority_subversion=0.15,
        sanctity_degradation=0.10
    ),

    "conservative_government": MoralFoundations(
        care_harm=0.20,
        fairness_cheating=0.20,
        loyalty_betrayal=0.25,
        authority_subversion=0.25,
        sanctity_degradation=0.10
    ),

    "academic_ethics_board": MoralFoundations(
        care_harm=0.35,
        fairness_cheating=0.30,
        loyalty_betrayal=0.05,
        authority_subversion=0.15,
        sanctity_degradation=0.15
    ),

    "civil_liberties_group": MoralFoundations(
        care_harm=0.25,
        fairness_cheating=0.30,
        loyalty_betrayal=0.05,
        authority_subversion=0.15,
        sanctity_degradation=0.25
    ),

    "national_security_agency": MoralFoundations(
        care_harm=0.25,
        fairness_cheating=0.15,
        loyalty_betrayal=0.35,
        authority_subversion=0.20,
        sanctity_degradation=0.05
    ),

    "multinational_corporation": MoralFoundations(
        care_harm=0.15,
        fairness_cheating=0.25,
        loyalty_betrayal=0.15,
        authority_subversion=0.35,
        sanctity_degradation=0.10
    ),

    "small_business_coalition": MoralFoundations(
        care_harm=0.20,
        fairness_cheating=0.40,
        loyalty_betrayal=0.15,
        authority_subversion=0.20,
        sanctity_degradation=0.05
    ),

    "international_standards_body": MoralFoundations(
        care_harm=0.30,
        fairness_cheating=0.30,
        loyalty_betrayal=0.10,
        authority_subversion=0.20,
        sanctity_degradation=0.10
    )
}


# ============================================================================
# EXAMPLE USAGE AND VALIDATION
# ============================================================================

def create_example_policy() -> PolicyFeatures:
    """
    Example: Mandatory AI Safety Testing Policy
    Models the EU AI Act high-risk system requirements
    """
    return PolicyFeatures(
        policy_id="P001",
        policy_name="Mandatory Pre-Deployment Safety Testing for High-Risk AI",
        policy_type="regulation",

        # High safety focus
        safety_requirements=0.85,
        harm_prevention=0.80,
        vulnerable_protection=0.75,
        privacy_safeguards=0.70,

        # Moderate fairness
        equity_provisions=0.60,
        procedural_fairness=0.75,
        access_equality=0.65,
        small_actor_burden=0.70,  # Burdensome for small companies

        # Mixed loyalty effects
        national_advantage=0.50,
        competitiveness_impact=0.60,  # Could harm competitiveness
        cross_border_cooperation=0.70,
        ingroup_solidarity=0.55,

        # Strong authority
        institutional_clarity=0.80,
        regulatory_strength=0.85,
        precedent_alignment=0.75,
        expert_deference=0.80,

        # Moderate sanctity
        human_dignity=0.70,
        privacy_sanctity=0.70,
        transparency_norms=0.75,
        manipulation_prevention=0.75,

        # Meta-attributes
        implementation_cost=0.65,
        innovation_impact=0.50,
        enforcement_difficulty=0.55
    )


def run_validation_example():
    """
    Demonstrate moral evaluation across different stakeholders
    """
    print("=" * 80)
    print("MORAL FOUNDATIONS MODULE - VALIDATION EXAMPLE")
    print("=" * 80)
    print()

    # Create policy and evaluator
    policy = create_example_policy()
    evaluator = MoralEvaluator(scenario_context="general")
    explainer = MoralExplainer(evaluator)

    # Evaluate from different stakeholder perspectives
    stakeholders = [
        ("consumer_advocacy_ngo", "Consumer Rights Alliance"),
        ("tech_industry_association", "Tech Industry Group"),
        ("conservative_government", "National Regulatory Authority"),
        ("academic_ethics_board", "University Ethics Board")
    ]

    for profile_key, agent_name in stakeholders:
        foundations = STAKEHOLDER_PROFILES[profile_key]

        print(f"\n{'=' * 80}")
        print(explainer.explain_evaluation(policy, foundations, agent_name))

        # Check for moral constraints
        is_admissible, violations = evaluator.check_moral_constraints(
            policy, foundations, threshold=-0.6
        )

        if not is_admissible:
            print(f"\n⚠️  MORAL CONSTRAINTS VIOLATED:")
            for violation in violations:
                print(f"   {violation}")
        else:
            print(f"\n✓ Policy is morally admissible for {agent_name}")

    print("\n" + "=" * 80)
    print("MORAL DISTANCE MATRIX")
    print("=" * 80)
    print("\nMoral similarity between stakeholders (lower = more similar):\n")

    # Compute pairwise moral distances
    profile_list = list(stakeholders)
    for i, (key1, name1) in enumerate(profile_list):
        for key2, name2 in profile_list[i+1:]:
            distance = STAKEHOLDER_PROFILES[key1].distance_to(STAKEHOLDER_PROFILES[key2])
            print(f"{name1} ↔ {name2}: {distance:.3f}")


if __name__ == "__main__":
    run_validation_example()
