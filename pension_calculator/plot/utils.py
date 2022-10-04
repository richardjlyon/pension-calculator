def currency(x, pos):
    """Format y axis currency label as £xxK"""
    if x >= 1e6:
        return "£{:1.1f}M".format(x * 1e-6)
    else:
        return "£{:1.0f}K".format(x * 1e-3)
