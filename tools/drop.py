import pickle, os
HERE = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(HERE, "plan2.pkl")
plan = pickle.load(open(p, "rb"))
plan = [(ci, n) for ci, n in plan if ci not in (1139, 886, 449)]
pickle.dump(plan, open(p, "wb"))
print(len(plan))
