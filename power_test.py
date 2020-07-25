def power_law(x):
	expe = 0
	prob_sum = 0
	fine = 50
	for i in range(fine):
		prob_sum += (1/(i+1)) ** (x)
		expe += (i+1) / fine * ((1/(i+1)) ** (x)) 

#	print( 'Current dist:', ((1/fine) ** x )/ prob_sum)
	return  expe/prob_sum



def find_power(DExpe):
	Upper = 50
	Lower = 0.1

	while Upper - Lower > 0.00001:
		diff = power_law( (Upper + Lower )/ 2) - DExpe
		if diff > 0:
			Lower = (Upper + Lower) / 2
		else:
			Upper = (Upper + Lower) / 2

	return (Lower + Upper) / 2


def power_prob_array(X):
	pwr = find_power(X)
	lst = [ (1/ (i+1)) ** pwr for i in range(50)]
	lst = [n /sum(lst) for n in lst]
	return lst

def test_func():
	S = 0
	lst = power_prob_array(0.45)

	for i in range(50):
		S += lst[i] * (i+1)/50
	print(S)

print(find_power(0.45),find_power(0.4),find_power(0.3))