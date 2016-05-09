This code will perform a two-tailed t-test for crime rate on holiday and average crime rate per day for a city.

We picked some holidays where we expect a significant trend. Some of them are federal holidays, some are observances.


Why two-tailed t-test?
We have less than 30 samples (less than 30 years of data) so we picked t-test over z-test. Two-tailed because we expect the data is normally distributed and evenly distributed around mean.

1. We choose significance level of 0.05.

2. We claim a null hypothesis that crime rate on holiday is same as average crime rate per day.
3. 
We propose an alternate hypothesis that crime rate on holiday varies from average crime rate per day.

The t-test should help to conclude which holidays are significant.


Interpretation of results:
If we get a p-value such as 0.03 (i.e., p = .03). This means that there is a 3% chance of finding a difference as large as (or larger than) the one in our data given that the null hypothesis is true. However, we want to know whether this is "statistically significant". Typically, if there is a 5% or less chance (5 times in 100 or less) that the difference in the average crime rate per day and average crime rate on holiday is as different as observed given the null hypothesis is true, we would reject the null hypothesis and accept the alternative hypothesis. Alternately, if the chance is greater than 5% (5 times in 100 or more), we would fail to reject the null hypothesis and would not accept the alternative hypothesis. As such, in this example where p = .03, we would reject the null hypothesis and accept the alternative hypothesis. We reject it because at a significance level of 0.03 (i.e., less than a 5% chance), the result we obtained could happen too frequently for us to be confident that it was the two average crime counts were the same.

Conclusion:
We performed t-test for 3 cities namely: Boston, Denver and Philadelphia as they have more than 1 sample to be tested. Unfortunately we could not perform t-test on Chicago and New York as they have data for just one year. From the observed p-values we can conclude that crime count on holidays like "Thanksgiving" and "Christmas" is less than that respective city's average crime per day count. In general, both these occassions are such where people are usually at home. So less the people on streets less is the crime. This is just one trend we observed. This data can be leveraged in future to make more accurate crime predictions. For eg: crime weights can be modified on such calendar days and predictions can tend to be precise.

Reference:
https://statistics.laerd.com/statistical-guides/hypothesis-testing-3.php
http://study.com/academy/lesson/z-test-t-test-similarities-differences.html