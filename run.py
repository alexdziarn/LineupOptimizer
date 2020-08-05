import pandas as pd
import pulp

print("running optimization")
# create datatable
da = pd.read_excel('DFS.xls')
df = pd.DataFrame(da, columns=["Name", "Price", "Value", "Pos"])

# create Problem
prob = pulp.LpProblem("ExpectedScore", pulp.LpMaximize)

# create list of players
players = list(df["Name"])

# create dict of prices
prices = dict(zip(players, df["Price"]))

# create dict of values/expected fantasy points
values = dict(zip(players, df["Value"]))

# create dict of posistions
positions = dict(zip(players, df["Pos"]))

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

# print the status
print(pulp.LpStatus[prob.status])

# print the optimal lineup
for z in prob.variables():
    if z.varValue > 0:
        print(z.name[6:] + " = " + str(z.varValue))

# print expected fantasy point total
print("Expected Score: " + str(pulp.value(prob.objective)))
