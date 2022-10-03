def compute_total_payments(
    growth_rate: float, years: int, initial_payment: float
) -> float:
    """
    Compute the total payment arising from an annual payment increasing at
    a defined rate for a defined number of years.

    Parameters
    ----------
    growth_rate Compound annual growth rate
    years Number of years payments are made
    initial_payment The payment in the first year

    Returns
    -------
    The total amount paid
    """
    total = 0
    for i in range(years):
        total += initial_payment * pow(1 + growth_rate, i)
    return total
