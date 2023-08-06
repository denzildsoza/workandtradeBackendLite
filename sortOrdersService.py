def sortArrayByProximityToBase(data):
    return sorted(data, key=lambda x: (abs(x['level'] - x['base']))/ x['base'])



# Example usage:
data = [19483, 19505, 19522, 19527, 19553]  # Example array
orders = [
    {'level':19418,'base':19517},
    {'level':19420,'base':19517},
    {'level':19522,'base':19517},
    {'level':19527,'base':19517},
    {'level':44880,'base':44879},
    {'level':44794,'base':44879},
    {'level':44810,'base':44879},
]




sortedData = sortArrayByProximityToBase(orders)
print(sortedData)


