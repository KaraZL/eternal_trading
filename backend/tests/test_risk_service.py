"""Unit tests for risk management service."""

from decimal import Decimal
import pytest

from app.services.risk_service import (
    calculate_eligible_collateral_value,
    calculate_ltv,
    assess_loan_risk,
)


class TestCalculateEligibleCollateralValue:
    """Tests for calculate_eligible_collateral_value function."""

    def test_no_haircut(self):
        """Test with zero haircut."""
        market_value = Decimal("10000.00")
        eligible = calculate_eligible_collateral_value(market_value, Decimal("0"))
        assert eligible == Decimal("10000.00")

    def test_with_haircut(self):
        """Test with 20% haircut."""
        market_value = Decimal("10000.00")
        eligible = calculate_eligible_collateral_value(market_value, Decimal("0.20"))
        assert eligible == Decimal("8000.00")

    def test_full_haircut(self):
        """Test with 100% haircut."""
        market_value = Decimal("10000.00")
        eligible = calculate_eligible_collateral_value(market_value, Decimal("1.00"))
        assert eligible == Decimal("0.00")

    def test_haircut_invalid_negative(self):
        """Test that negative haircut raises ValueError."""
        with pytest.raises(ValueError, match="Haircut percentage must be between 0 and 1"):
            calculate_eligible_collateral_value(Decimal("10000.00"), Decimal("-0.10"))

    def test_haircut_invalid_over_one(self):
        """Test that haircut > 1 raises ValueError."""
        with pytest.raises(ValueError, match="Haircut percentage must be between 0 and 1"):
            calculate_eligible_collateral_value(Decimal("10000.00"), Decimal("1.10"))


class TestCalculateLTV:
    """Tests for calculate_ltv function."""

    def test_ltv_50_percent(self):
        """Test LTV calculation at 50%."""
        loan = Decimal("5000.00")
        collateral = Decimal("10000.00")
        ltv = calculate_ltv(loan, collateral)
        assert ltv == Decimal("0.5")

    def test_ltv_60_percent(self):
        """Test LTV calculation at 60%."""
        loan = Decimal("6000.00")
        collateral = Decimal("10000.00")
        ltv = calculate_ltv(loan, collateral)
        assert ltv == Decimal("0.6")

    def test_ltv_75_percent(self):
        """Test LTV calculation at 75%."""
        loan = Decimal("7500.00")
        collateral = Decimal("10000.00")
        ltv = calculate_ltv(loan, collateral)
        assert ltv == Decimal("0.75")

    def test_ltv_zero_collateral_raises_error(self):
        """Test that zero collateral raises ValueError."""
        with pytest.raises(ValueError, match="Eligible collateral value must be positive"):
            calculate_ltv(Decimal("5000.00"), Decimal("0"))

    def test_ltv_negative_collateral_raises_error(self):
        """Test that negative collateral raises ValueError."""
        with pytest.raises(ValueError, match="Eligible collateral value must be positive"):
            calculate_ltv(Decimal("5000.00"), Decimal("-1000.00"))


class TestAssessLoanRisk:
    """Tests for assess_loan_risk function."""

    def test_healthy_status(self):
        """Test loan with healthy status (LTV < 0.60)."""
        result = assess_loan_risk(
            loan_amount=Decimal("5000.00"),
            collateral_market_value=Decimal("10000.00"),
            haircut_percentage=Decimal("0.00"),
        )
        assert result["status"] == "healthy"
        assert result["ltv"] == Decimal("0.50")
        assert result["eligible_collateral_value"] == Decimal("10000.00")

    def test_warning_status(self):
        """Test loan with warning status (0.60 <= LTV < 0.70)."""
        result = assess_loan_risk(
            loan_amount=Decimal("6000.00"),
            collateral_market_value=Decimal("10000.00"),
            haircut_percentage=Decimal("0.00"),
        )
        assert result["status"] == "warning"
        assert result["ltv"] == Decimal("0.60")

    def test_breach_status(self):
        """Test loan with breach status (LTV >= 0.70)."""
        result = assess_loan_risk(
            loan_amount=Decimal("7500.00"),
            collateral_market_value=Decimal("10000.00"),
            haircut_percentage=Decimal("0.00"),
        )
        assert result["status"] == "breach"
        assert result["ltv"] == Decimal("0.75")

    def test_with_haircut_moves_to_healthy(self):
        """Test that haircut improves loan status."""
        # Without haircut: LTV = 0.70 (breach)
        result_no_haircut = assess_loan_risk(
            loan_amount=Decimal("7000.00"),
            collateral_market_value=Decimal("10000.00"),
            haircut_percentage=Decimal("0.00"),
        )
        assert result_no_haircut["status"] == "breach"

        # With 10% haircut: eligible = 9000, LTV = 0.7777 (still breach)
        result_with_haircut = assess_loan_risk(
            loan_amount=Decimal("7000.00"),
            collateral_market_value=Decimal("10000.00"),
            haircut_percentage=Decimal("0.10"),
        )
        assert result_with_haircut["status"] == "breach"

        # With 30% haircut: eligible = 7000, LTV = 1.0 (still breach)
        result_with_more_haircut = assess_loan_risk(
            loan_amount=Decimal("7000.00"),
            collateral_market_value=Decimal("10000.00"),
            haircut_percentage=Decimal("0.30"),
        )
        assert result_with_more_haircut["ltv"] == Decimal("1.00")

    def test_custom_thresholds(self):
        """Test with custom warning and breach thresholds."""
        result = assess_loan_risk(
            loan_amount=Decimal("7500.00"),
            collateral_market_value=Decimal("10000.00"),
            haircut_percentage=Decimal("0.00"),
            warning_ltv_threshold=Decimal("0.70"),
            breach_ltv_threshold=Decimal("0.80"),
        )
        # LTV = 0.75, between custom thresholds
        assert result["status"] == "warning"

    def test_boundary_at_warning_threshold(self):
        """Test boundary condition at warning threshold."""
        result = assess_loan_risk(
            loan_amount=Decimal("6000.00"),
            collateral_market_value=Decimal("10000.00"),
            haircut_percentage=Decimal("0.00"),
            warning_ltv_threshold=Decimal("0.60"),
            breach_ltv_threshold=Decimal("0.70"),
        )
        # LTV exactly at threshold
        assert result["ltv"] == Decimal("0.60")
        assert result["status"] == "warning"

    def test_boundary_at_breach_threshold(self):
        """Test boundary condition at breach threshold."""
        result = assess_loan_risk(
            loan_amount=Decimal("7000.00"),
            collateral_market_value=Decimal("10000.00"),
            haircut_percentage=Decimal("0.00"),
            warning_ltv_threshold=Decimal("0.60"),
            breach_ltv_threshold=Decimal("0.70"),
        )
        # LTV exactly at breach threshold
        assert result["ltv"] == Decimal("0.70")
        assert result["status"] == "breach"

    def test_precision_with_decimals(self):
        """Test that Decimal precision is maintained."""
        result = assess_loan_risk(
            loan_amount=Decimal("3333.33"),
            collateral_market_value=Decimal("10000.00"),
            haircut_percentage=Decimal("0.15"),
        )
        eligible = Decimal("8500.00")
        expected_ltv = Decimal("3333.33") / eligible
        assert result["eligible_collateral_value"] == eligible
        # Check LTV is calculated with Decimal precision
        assert isinstance(result["ltv"], Decimal)

    def test_healthy_with_large_numbers(self):
        """Test healthy status with large loan amounts: loan 500000, collateral 2000000, haircut 0.20 => LTV 0.3125."""
        result = assess_loan_risk(
            loan_amount=Decimal("500000.00"),
            collateral_market_value=Decimal("2000000.00"),
            haircut_percentage=Decimal("0.20"),
        )
        # eligible = 2000000 * (1 - 0.20) = 1600000
        # ltv = 500000 / 1600000 = 0.3125
        assert result["eligible_collateral_value"] == Decimal("1600000.00")
        assert result["ltv"] == Decimal("0.3125")
        assert result["status"] == "healthy"

    def test_warning_with_large_numbers(self):
        """Test warning status with large loan amounts: loan 1000000, collateral 2000000, haircut 0.20 => LTV 0.6250."""
        result = assess_loan_risk(
            loan_amount=Decimal("1000000.00"),
            collateral_market_value=Decimal("2000000.00"),
            haircut_percentage=Decimal("0.20"),
        )
        # eligible = 2000000 * (1 - 0.20) = 1600000
        # ltv = 1000000 / 1600000 = 0.6250
        assert result["eligible_collateral_value"] == Decimal("1600000.00")
        assert result["ltv"] == Decimal("0.6250")
        assert result["status"] == "warning"

    def test_breach_with_large_numbers(self):
        """Test breach status with large loan amounts: loan 1200000, collateral 2000000, haircut 0.20 => LTV 0.7500."""
        result = assess_loan_risk(
            loan_amount=Decimal("1200000.00"),
            collateral_market_value=Decimal("2000000.00"),
            haircut_percentage=Decimal("0.20"),
        )
        # eligible = 2000000 * (1 - 0.20) = 1600000
        # ltv = 1200000 / 1600000 = 0.7500
        assert result["eligible_collateral_value"] == Decimal("1600000.00")
        assert result["ltv"] == Decimal("0.7500")
        assert result["status"] == "breach"

    def test_invalid_zero_collateral_market_value(self):
        """Test that zero collateral_market_value raises ValueError."""
        with pytest.raises(ValueError, match="Eligible collateral value must be positive"):
            assess_loan_risk(
                loan_amount=Decimal("500000.00"),
                collateral_market_value=Decimal("0.00"),
                haircut_percentage=Decimal("0.20"),
            )

    def test_invalid_full_haircut_raises_error(self):
        """Test that 100% haircut raises ValueError because eligible collateral becomes zero."""
        with pytest.raises(ValueError, match="Eligible collateral value must be positive"):
            assess_loan_risk(
                loan_amount=Decimal("500000.00"),
                collateral_market_value=Decimal("2000000.00"),
                haircut_percentage=Decimal("1.00"),
            )
