import pickle

with open('mfui.pickle', 'rb') as handle:
    unserialized_mfui = pickle.load(handle)

print(unserialized_mfui, len(unserialized_mfui))



with open('trui.pickle', 'rb') as handle:
    unserialized_trui = pickle.load(handle)

print(unserialized_trui, len(unserialized_trui))