from scipy import stats

def main():
	# Analysis for crimes are more in summer as compare to winter.
	# summer month from June to September
	# winter months from October to May 
	# here sum_bos and win_bos presents the crime data for these months Similary we have same data sets for cities.

	sum_bos = [6024,8081,7285,6587]
	win_bos = [5327,4025,5107,5307,6073,6603,5930,5875]

	two_sample_bos = stats.ttest_ind(sum_bos, win_bos,equal_var=False)
	print "Boston : The t-statistic is %.3f and the p-value is %.3f." % two_sample_bos

	sum_phi = [24175,24655,24835,24276]
	win_phi = [20917,18418,21122,22248,25019,24764,21510,20495]

	two_sample_phi = stats.ttest_ind(sum_phi, win_phi,equal_var=False)
	print "Philly : The t-statistic is %.3f and the p-value is %.3f." % two_sample_phi

	sum_den = [4824,5379,5362,4804]
	win_den = [4826,3998,3928,3913,4516,4702,4122,4045]
	

	two_sample_den = stats.ttest_ind(sum_den, win_den,equal_var=False)
	print "Denver : The t-statistic is %.3f and the p-value is %.3f." % two_sample_den	

	sum_chi = [2135,2338,2368,2141]
	win_chi = [1799,1327,2025,2004,2193,2131,1825,1981]

	two_sample_chi = stats.ttest_ind(sum_chi, win_chi,equal_var=False)
	print "Chicago : The t-statistic is %.3f and the p-value is %.3f." % two_sample_chi	

	sum_ny = [8436,9473,9677,8264]
	win_ny = [7697,6408,7425,7892,8826]

	two_sample_ny = stats.ttest_ind(sum_ny, win_ny,equal_var=False)
	print "New York : The t-statistic is %.3f and the p-value is %.3f." % two_sample_ny

# Analysis for crimes are more in daylight saving months as compare to non- daylight saving months.
	# daylight saving month from March to November
	# Non- daylight saving month from December to February. 
	# here d_sum_bos and d_win_bos presents the crime data for these months Similary we have same data sets for cities.

	d_sum_bos = [5107,5307,6073,6024,8081,7285,6587,6603,5930]
	d_win_bos = [5327,4025,5875]

	d_two_sample_bos = stats.ttest_ind(d_sum_bos, d_win_bos,equal_var=False)
	print "Boston dayLight : The t-statistic is %.3f and the p-value is %.3f." % d_two_sample_bos	

	d_sum_phi = [21122,22248,25019,24175,24655,24834,24276,24764,21510]
	d_win_phi = [20917,18418,20495]

	d_two_sample_phi = stats.ttest_ind(d_sum_phi, d_win_phi,equal_var=False)
	print "Philly dayLight : The t-statistic is %.3f and the p-value is %.3f." % d_two_sample_phi

	d_sum_chi = [2025,2004,2193,2135,2338,2368,2141,2131,1825]
	d_win_chi = [1799,1327,1981]

	d_two_sample_chi = stats.ttest_ind(d_sum_chi, d_win_chi,equal_var=False)
	print "Chicago dayLight : The t-statistic is %.3f and the p-value is %.3f." % d_two_sample_chi

	d_sum_den = [3928,3913,4516,4824,5379,5362,4804,4702,4122]
	d_win_den = [4826,3998,4045]

	d_two_sample_den = stats.ttest_ind(d_sum_den, d_win_den,equal_var=False)
	print "Denver dayLight : The t-statistic is %.3f and the p-value is %.3f." % d_two_sample_den

	d_sum_ny = [7425,7892,8826,8436,9473,9677,8264]
	d_win_ny = [7697,6408]

	d_two_sample_ny = stats.ttest_ind(d_sum_ny, d_win_ny,equal_var=False)
	print "New York dayLight : The t-statistic is %.3f and the p-value is %.3f." % d_two_sample_ny


if __name__ == "__main__":
	main()

