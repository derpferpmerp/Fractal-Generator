import numpy as np


def hidePlotBounds(ax):
	ax.spines['top'].set_visible(False)
	ax.spines['right'].set_visible(False)
	ax.spines['bottom'].set_visible(False)
	ax.spines['left'].set_visible(False)

	ax.set_xticklabels([])
	ax.set_yticklabels([])

	ax.set_xticks([])
	ax.set_yticks([])

	ax.axes.get_xaxis().set_visible(False)
	ax.axes.get_yaxis().set_visible(False)

def constructBounds(lst, tau=0.1):
	# LST : [ ( ( R, G, B ), INDX ) ... ]
	# Tau : Mult of Distance for Spacing, D*(1-tau) < D < D*(1+tau) 
	lstSorted = sorted(lst, key=lambda x: x[1])
	lstSorted = [ (x[0], x[1] * np.array([1-tau, 1+tau])) for x in lstSorted]
	FINALBOUNDS = []
	FINALCOLORS = []
	for i in range(len(lstSorted)):
		choice = "L" if (i == len(lstSorted) - 1) else ("F" if i==0 else "M")
		item = lstSorted[i]
		if i > 0:
			if sorted(item[0]) == sorted(FINALCOLORS[-1]):
				continue
			else:
				j = FINALBOUNDS[-1]
				print(j, type(j))
		if choice == "F":
			FINALBOUNDS.append(item[1][0])
		elif choice == "L":
			FINALBOUNDS.append(item[1][0])
			FINALBOUNDS.append(item[1][-1])
		elif choice == "M":
			I = item[1][0]
			if I != FINALBOUNDS[-1]:
				FINALBOUNDS.append(item[1][0])
		FINALCOLORS.append(item[0])
	print(FINALBOUNDS)
	return FINALBOUNDS, FINALCOLORS