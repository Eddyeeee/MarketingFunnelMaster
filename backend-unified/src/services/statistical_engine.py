"""
Statistical Analysis Engine for A/B Testing
Module: 2C - Conversion & Marketing Automation
Created: 2025-07-04

Advanced statistical analysis for A/B testing including significance testing,
confidence intervals, power analysis, and early stopping rules.
"""

import numpy as np
from scipy import stats
from scipy.stats import beta
import math
from typing import Dict, Tuple, Optional, List
from dataclasses import dataclass
from enum import Enum

class TestType(str, Enum):
    FREQUENTIST = "frequentist"
    BAYESIAN = "bayesian"
    SEQUENTIAL = "sequential"

@dataclass
class StatisticalResult:
    """Container for statistical test results"""
    p_value: float
    confidence_interval: Tuple[float, float]
    effect_size: float
    lift: float
    is_significant: bool
    test_statistic: float
    degrees_of_freedom: Optional[int] = None
    bayesian_probability: Optional[float] = None

class StatisticalEngine:
    """Advanced statistical analysis engine for A/B testing"""
    
    def __init__(self):
        self.alpha_levels = {
            0.90: 0.10,
            0.95: 0.05,
            0.99: 0.01
        }
    
    def calculate_sample_size(self, 
                            baseline_rate: float, 
                            minimum_detectable_effect: float,
                            confidence_level: float = 0.95,
                            statistical_power: float = 0.80) -> int:
        """
        Calculate required sample size for A/B test
        
        Args:
            baseline_rate: Expected conversion rate for control
            minimum_detectable_effect: Minimum effect size to detect (e.g., 0.05 for 5% relative change)
            confidence_level: Statistical confidence level (0.90, 0.95, 0.99)
            statistical_power: Desired statistical power (typically 0.80 or 0.90)
        
        Returns:
            Required sample size per variant
        """
        
        alpha = self.alpha_levels[confidence_level]
        beta = 1 - statistical_power
        
        # Calculate effect size (Cohen's h for proportions)
        p1 = baseline_rate
        p2 = baseline_rate * (1 + minimum_detectable_effect)
        
        # Ensure p2 doesn't exceed 1.0
        p2 = min(p2, 0.99)
        
        # Cohen's h effect size
        h = 2 * (math.asin(math.sqrt(p2)) - math.asin(math.sqrt(p1)))
        
        # Z-scores for alpha and beta
        z_alpha = stats.norm.ppf(1 - alpha/2)
        z_beta = stats.norm.ppf(1 - beta)
        
        # Sample size calculation
        n = ((z_alpha + z_beta) / h) ** 2
        
        # Apply finite population correction and round up
        n_adjusted = math.ceil(n * 1.1)  # 10% safety margin
        
        return max(n_adjusted, 100)  # Minimum 100 per variant
    
    def calculate_significance(self,
                             control_conversions: int,
                             control_participants: int,
                             variant_conversions: int,
                             variant_participants: int,
                             confidence_level: float = 0.95,
                             test_type: TestType = TestType.FREQUENTIST) -> Dict:
        """
        Calculate statistical significance between control and variant
        
        Args:
            control_conversions: Number of conversions in control
            control_participants: Number of participants in control
            variant_conversions: Number of conversions in variant
            variant_participants: Number of participants in variant
            confidence_level: Statistical confidence level
            test_type: Type of statistical test to perform
        
        Returns:
            Dictionary with test results
        """
        
        if test_type == TestType.FREQUENTIST:
            return self._frequentist_test(
                control_conversions, control_participants,
                variant_conversions, variant_participants,
                confidence_level
            )
        elif test_type == TestType.BAYESIAN:
            return self._bayesian_test(
                control_conversions, control_participants,
                variant_conversions, variant_participants,
                confidence_level
            )
        else:
            return self._sequential_test(
                control_conversions, control_participants,
                variant_conversions, variant_participants,
                confidence_level
            )
    
    def _frequentist_test(self,
                         control_conversions: int,
                         control_participants: int,
                         variant_conversions: int,
                         variant_participants: int,
                         confidence_level: float) -> Dict:
        """Perform frequentist statistical test (Z-test for proportions)"""
        
        # Calculate conversion rates
        p1 = control_conversions / max(control_participants, 1)
        p2 = variant_conversions / max(variant_participants, 1)
        
        # Calculate pooled proportion
        pooled_conversions = control_conversions + variant_conversions
        pooled_participants = control_participants + variant_participants
        pooled_p = pooled_conversions / max(pooled_participants, 1)
        
        # Calculate standard error
        se = math.sqrt(pooled_p * (1 - pooled_p) * (1/max(control_participants, 1) + 1/max(variant_participants, 1)))
        
        # Calculate test statistic
        if se == 0:
            z_stat = 0
            p_value = 1.0
        else:
            z_stat = (p2 - p1) / se
            p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))
        
        # Calculate confidence interval for difference
        se_diff = math.sqrt(p1 * (1 - p1) / max(control_participants, 1) + 
                           p2 * (1 - p2) / max(variant_participants, 1))
        
        alpha = self.alpha_levels[confidence_level]
        z_critical = stats.norm.ppf(1 - alpha/2)
        
        diff = p2 - p1
        margin_error = z_critical * se_diff
        ci_lower = diff - margin_error
        ci_upper = diff + margin_error
        
        # Calculate lift percentage
        lift = ((p2 - p1) / max(p1, 0.001)) * 100 if p1 > 0 else 0
        
        # Effect size (Cohen's h)
        if p1 > 0 and p2 > 0:
            effect_size = 2 * (math.asin(math.sqrt(p2)) - math.asin(math.sqrt(p1)))
        else:
            effect_size = 0
        
        return {
            "test_type": "frequentist",
            "p_value": p_value,
            "z_statistic": z_stat,
            "confidence_interval": (ci_lower, ci_upper),
            "effect_size": effect_size,
            "lift": lift,
            "is_significant": p_value < self.alpha_levels[confidence_level],
            "control_rate": p1,
            "variant_rate": p2,
            "relative_improvement": lift,
            "absolute_improvement": (p2 - p1) * 100,
            "confidence_level": confidence_level,
            "degrees_of_freedom": None
        }
    
    def _bayesian_test(self,
                      control_conversions: int,
                      control_participants: int,
                      variant_conversions: int,
                      variant_participants: int,
                      confidence_level: float) -> Dict:
        """Perform Bayesian A/B test using Beta-Binomial model"""
        
        # Use Beta(1,1) as non-informative prior
        alpha_prior = 1
        beta_prior = 1
        
        # Calculate posterior parameters
        alpha_control = alpha_prior + control_conversions
        beta_control = beta_prior + (control_participants - control_conversions)
        
        alpha_variant = alpha_prior + variant_conversions
        beta_variant = beta_prior + (variant_participants - variant_conversions)
        
        # Calculate probability that variant is better than control
        # Using Monte Carlo sampling
        n_samples = 10000
        control_samples = beta.rvs(alpha_control, beta_control, size=n_samples)
        variant_samples = beta.rvs(alpha_variant, beta_variant, size=n_samples)
        
        prob_variant_better = np.mean(variant_samples > control_samples)
        
        # Calculate credible interval for the difference
        diff_samples = variant_samples - control_samples
        credible_interval = np.percentile(diff_samples, [2.5, 97.5])
        
        # Calculate posterior means
        control_rate = alpha_control / (alpha_control + beta_control)
        variant_rate = alpha_variant / (alpha_variant + beta_variant)
        
        # Calculate lift
        lift = ((variant_rate - control_rate) / max(control_rate, 0.001)) * 100 if control_rate > 0 else 0
        
        # Calculate effect size
        if control_rate > 0 and variant_rate > 0:
            effect_size = 2 * (math.asin(math.sqrt(variant_rate)) - math.asin(math.sqrt(control_rate)))
        else:
            effect_size = 0
        
        # Determine significance (typically 95% probability)
        significance_threshold = confidence_level
        is_significant = prob_variant_better > significance_threshold or prob_variant_better < (1 - significance_threshold)
        
        return {
            "test_type": "bayesian",
            "probability_variant_better": prob_variant_better,
            "credible_interval": tuple(credible_interval),
            "effect_size": effect_size,
            "lift": lift,
            "is_significant": is_significant,
            "control_rate": control_rate,
            "variant_rate": variant_rate,
            "relative_improvement": lift,
            "absolute_improvement": (variant_rate - control_rate) * 100,
            "confidence_level": confidence_level,
            "bayesian_probability": prob_variant_better
        }
    
    def _sequential_test(self,
                        control_conversions: int,
                        control_participants: int,
                        variant_conversions: int,
                        variant_participants: int,
                        confidence_level: float) -> Dict:
        """Perform sequential probability ratio test (SPRT)"""
        
        # For now, fall back to frequentist test
        # In production, implement proper SPRT with spending functions
        result = self._frequentist_test(
            control_conversions, control_participants,
            variant_conversions, variant_participants,
            confidence_level
        )
        result["test_type"] = "sequential"
        return result
    
    def calculate_confidence_interval(self,
                                    conversions: int,
                                    participants: int,
                                    confidence_level: float = 0.95) -> Tuple[float, float]:
        """Calculate confidence interval for a single proportion"""
        
        if participants == 0:
            return (0.0, 0.0)
        
        p = conversions / participants
        
        # Wilson score interval (more accurate for small samples)
        alpha = self.alpha_levels[confidence_level]
        z = stats.norm.ppf(1 - alpha/2)
        
        denominator = 1 + z**2 / participants
        center = (p + z**2 / (2 * participants)) / denominator
        margin = z * math.sqrt(p * (1 - p) / participants + z**2 / (4 * participants**2)) / denominator
        
        lower = max(0, center - margin)
        upper = min(1, center + margin)
        
        return (lower, upper)
    
    def calculate_power(self,
                       effect_size: float,
                       sample_size: int,
                       confidence_level: float = 0.95) -> float:
        """Calculate statistical power for given effect size and sample size"""
        
        alpha = self.alpha_levels[confidence_level]
        z_alpha = stats.norm.ppf(1 - alpha/2)
        z_beta = effect_size * math.sqrt(sample_size/2) - z_alpha
        
        power = stats.norm.cdf(z_beta)
        return max(0, min(1, power))
    
    def calculate_minimum_detectable_effect(self,
                                          sample_size: int,
                                          baseline_rate: float,
                                          confidence_level: float = 0.95,
                                          statistical_power: float = 0.80) -> float:
        """Calculate minimum detectable effect for given sample size"""
        
        alpha = self.alpha_levels[confidence_level]
        beta = 1 - statistical_power
        
        z_alpha = stats.norm.ppf(1 - alpha/2)
        z_beta = stats.norm.ppf(1 - beta)
        
        # Calculate standard error
        se = math.sqrt(2 * baseline_rate * (1 - baseline_rate) / sample_size)
        
        # Minimum detectable difference
        min_diff = (z_alpha + z_beta) * se
        
        # Convert to relative effect
        mde = min_diff / baseline_rate if baseline_rate > 0 else min_diff
        
        return mde
    
    def early_stopping_boundary(self,
                               current_sample_size: int,
                               max_sample_size: int,
                               alpha: float = 0.05,
                               spending_function: str = "obrien_fleming") -> float:
        """Calculate early stopping boundary using spending functions"""
        
        t = current_sample_size / max_sample_size  # Information fraction
        
        if spending_function == "obrien_fleming":
            # O'Brien-Fleming spending function
            if t <= 0:
                return float('inf')
            spending = 2 * (1 - stats.norm.cdf(stats.norm.ppf(1 - alpha/2) / math.sqrt(t)))
        elif spending_function == "pocock":
            # Pocock spending function
            spending = alpha * math.log(1 + (math.e - 1) * t)
        else:
            # Linear spending function
            spending = alpha * t
        
        # Convert spending to boundary
        if spending >= alpha:
            return 0  # Stop for efficacy
        else:
            return stats.norm.ppf(1 - spending/2)
    
    def futility_boundary(self,
                         current_sample_size: int,
                         max_sample_size: int,
                         beta: float = 0.20) -> float:
        """Calculate futility stopping boundary"""
        
        t = current_sample_size / max_sample_size
        
        # Conservative futility boundary
        if t < 0.5:
            return float('-inf')  # No futility stopping before halfway
        
        # Linear beta spending
        spent_beta = beta * (t - 0.5) / 0.5
        return stats.norm.ppf(spent_beta)
    
    def meta_analysis(self, test_results: List[Dict]) -> Dict:
        """Perform meta-analysis across multiple A/B tests"""
        
        if not test_results:
            return {"error": "No test results provided"}
        
        # Extract effect sizes and standard errors
        effect_sizes = []
        standard_errors = []
        sample_sizes = []
        
        for result in test_results:
            if 'effect_size' in result and 'control_participants' in result and 'variant_participants' in result:
                effect_sizes.append(result['effect_size'])
                
                # Estimate standard error from sample size
                n_total = result['control_participants'] + result['variant_participants']
                se = math.sqrt(2 / n_total)  # Approximate SE for Cohen's h
                standard_errors.append(se)
                sample_sizes.append(n_total)
        
        if not effect_sizes:
            return {"error": "No valid effect sizes found"}
        
        # Fixed-effects meta-analysis
        weights = [1/se**2 for se in standard_errors]
        weighted_mean = sum(es * w for es, w in zip(effect_sizes, weights)) / sum(weights)
        pooled_se = 1 / math.sqrt(sum(weights))
        
        # Test for overall effect
        z_stat = weighted_mean / pooled_se
        p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))
        
        # Heterogeneity test (Q statistic)
        q_stat = sum(w * (es - weighted_mean)**2 for es, w in zip(effect_sizes, weights))
        df = len(effect_sizes) - 1
        heterogeneity_p = 1 - stats.chi2.cdf(q_stat, df) if df > 0 else 1.0
        
        # I² statistic
        i_squared = max(0, (q_stat - df) / q_stat) if q_stat > 0 else 0
        
        return {
            "pooled_effect_size": weighted_mean,
            "standard_error": pooled_se,
            "z_statistic": z_stat,
            "p_value": p_value,
            "is_significant": p_value < 0.05,
            "heterogeneity": {
                "q_statistic": q_stat,
                "p_value": heterogeneity_p,
                "i_squared": i_squared,
                "interpretation": "low" if i_squared < 0.25 else "moderate" if i_squared < 0.75 else "high"
            },
            "number_of_tests": len(effect_sizes),
            "total_sample_size": sum(sample_sizes)
        }
    
    def bayesian_meta_analysis(self, test_results: List[Dict]) -> Dict:
        """Perform Bayesian meta-analysis across multiple A/B tests"""
        
        # Simplified Bayesian meta-analysis
        # In production, use proper hierarchical Bayesian models
        
        all_control_conversions = sum(r.get('control_conversions', 0) for r in test_results)
        all_control_participants = sum(r.get('control_participants', 0) for r in test_results)
        all_variant_conversions = sum(r.get('variant_conversions', 0) for r in test_results)
        all_variant_participants = sum(r.get('variant_participants', 0) for r in test_results)
        
        if all_control_participants == 0 or all_variant_participants == 0:
            return {"error": "Insufficient data for meta-analysis"}
        
        return self._bayesian_test(
            all_control_conversions, all_control_participants,
            all_variant_conversions, all_variant_participants,
            0.95
        )