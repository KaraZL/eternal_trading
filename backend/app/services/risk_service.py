"""Risk management service for loan LTV calculations."""

from decimal import Decimal, InvalidOperation


def calculate_eligible_collateral_value(
    collateral_market_value: Decimal, haircut_percentage: Decimal
) -> Decimal:
    """
    Calculate eligible collateral value after applying haircut.

    eligible_collateral_value = collateral_market_value * (1 - haircut_percentage)

    Args:
        collateral_market_value: Market value of collateral
        haircut_percentage: Haircut percentage as decimal (0.0 to 1.0)

    Returns:
        Eligible collateral value after haircut

    Raises:
        ValueError: If haircut_percentage is outside valid range
    """
    if not Decimal(0) <= haircut_percentage <= Decimal(1):
        raise ValueError("Haircut percentage must be between 0 and 1")

    return collateral_market_value * (Decimal(1) - haircut_percentage)


def calculate_ltv(
    loan_amount: Decimal, eligible_collateral_value: Decimal
) -> Decimal:
    """
    Calculate Loan-to-Value (LTV) ratio.

    ltv = loan_amount / eligible_collateral_value

    Args:
        loan_amount: Amount of the loan
        eligible_collateral_value: Eligible collateral value after haircut

    Returns:
        LTV as Decimal

    Raises:
        ValueError: If eligible_collateral_value is zero or negative
    """
    if eligible_collateral_value <= 0:
        raise ValueError("Eligible collateral value must be positive")

    return (loan_amount / eligible_collateral_value).quantize(Decimal("0.0001"))


def assess_loan_risk(
    loan_amount: Decimal,
    collateral_market_value: Decimal,
    haircut_percentage: Decimal,
    warning_ltv_threshold: Decimal = Decimal("0.60"),
    breach_ltv_threshold: Decimal = Decimal("0.70"),
) -> dict:
    """
    Assess loan risk based on LTV.

    Args:
        loan_amount: Amount of the loan
        collateral_market_value: Market value of collateral
        haircut_percentage: Haircut percentage as decimal (0.0 to 1.0)
        warning_ltv_threshold: LTV threshold for warning (default 0.60)
        breach_ltv_threshold: LTV threshold for breach (default 0.70)

    Returns:
        Dictionary with:
            - eligible_collateral_value: Eligible collateral after haircut
            - ltv: Loan-to-Value ratio
            - status: "healthy", "warning", or "breach"

    Raises:
        ValueError: If inputs are invalid
    """
    eligible_collateral_value = calculate_eligible_collateral_value(
        collateral_market_value, haircut_percentage
    )
    ltv = calculate_ltv(loan_amount, eligible_collateral_value)

    # Determine status
    if ltv < warning_ltv_threshold:
        status = "healthy"
    elif ltv < breach_ltv_threshold:
        status = "warning"
    else:
        status = "breach"

    return {
        "eligible_collateral_value": eligible_collateral_value,
        "ltv": ltv,
        "status": status,
    }


def assess_loan_risk_with_collateral(
    loan: dict,
    collateral_items: list,
    warning_ltv_threshold: Decimal = Decimal("0.60"),
    breach_ltv_threshold: Decimal = Decimal("0.70"),
) -> dict:
    """
    Assess loan risk based on LTV using collateral items.

    Args:
        loan: Loan dictionary with amount and currency
        collateral_items: List of collateral dictionaries for the loan
        warning_ltv_threshold: LTV threshold for warning (default 0.60)
        breach_ltv_threshold: LTV threshold for breach (default 0.70)

    Returns:
        Dictionary with:
            - loan_id: Loan ID
            - loan_amount: Loan amount
            - total_market_value: Sum of all collateral market values
            - total_eligible_collateral_value: Sum of eligible collateral after haircuts
            - ltv: Loan-to-Value ratio
            - status: "healthy", "warning", or "breach"
            - collateral_count: Number of collateral items

    Raises:
        ValueError: If no collateral or invalid collateral data
    """
    if not collateral_items:
        raise ValueError("Loan has no collateral")

    loan_amount = loan["amount"]
    total_market_value = Decimal("0")
    total_eligible_value = Decimal("0")

    for collateral in collateral_items:
        market_value = collateral["market_value"]
        haircut = collateral["haircut_percentage"]

        total_market_value += market_value
        eligible = calculate_eligible_collateral_value(market_value, haircut)
        total_eligible_value += eligible

    ltv = calculate_ltv(loan_amount, total_eligible_value)

    # Determine status
    if ltv < warning_ltv_threshold:
        status = "healthy"
    elif ltv < breach_ltv_threshold:
        status = "warning"
    else:
        status = "breach"

    return {
        "loan_id": loan["id"],
        "loan_amount": loan_amount,
        "total_market_value": total_market_value,
        "total_eligible_collateral_value": total_eligible_value,
        "ltv": ltv,
        "status": status,
        "collateral_count": len(collateral_items),
    }
