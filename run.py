import pandas as pd
import pulp

print("running optimization")

def optimize(excelsheet, namecol, pricecol, valuecol, poscol):

    # create datatable
    da = pd.read_excel(excelsheet)
    df = pd.DataFrame(da, columns=[namecol, pricecol, valuecol, poscol])

    # create list of players
    players = list(df[namecol])

    # create dict of prices
    prices = dict(zip(players, df[pricecol]))

    # create dict of values/expected fantasy points
    values = dict(zip(players, df[valuecol]))

    # create dict of posistions
    positions = dict(zip(players, df[poscol]))
    
    # create Problem
    prob = pulp.LpProblem("ExpectedScore", pulp.LpMaximize)

    # create variables
    inout = pulp.LpVariable.dicts("inout", players, lowBound=0, cat="Binary")

    # objective function
    prob += pulp.lpSum([inout[x] * values[x] for x in players])

    # constraints
    salary = 60000
    prob += pulp.lpSum([inout[x] * prices[x] for x in players]) <= salary
    prob += pulp.lpSum([inout[x] for x in players if positions[x] == "PG"]) == 2
    prob += pulp.lpSum([inout[x] for x in players if positions[x] == "SG"]) == 2
    prob += pulp.lpSum([inout[x] for x in players if positions[x] == "SF"]) == 2
    prob += pulp.lpSum([inout[x] for x in players if positions[x] == "PF"]) == 2
    prob += pulp.lpSum([inout[x] for x in players if positions[x] == "C"]) == 1

    # solve
    prob.solve()


    # print the optimal lineup
    for z in prob.variables():
        if z.varValue > 0:
            print(z.name[6:])

    # print expected fantasy point total
    print("Expected Score: " + str(pulp.value(prob.objective)))

optimize("DFS.xls", "Name", "Price", "Value", "Pos")
