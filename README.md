# Xerox-Innovation-Contest
XRCI contest held on 12th oct - 25th oct 2015 on hackerrank
The aim of this challenge is to predict risk of death (mortality) in patients admitted to intensive care units (ICU) within hospitals.
#
Score :0.43/1.00
#
pos: 5/1500
#
Our approach in brief towards the problem was guided by 2 basic facts :-
#
a) The doctor knows the best
#
b) In general the trend of the vitals will ultimately determine the mortality rate for the majority of population

The features we created therefore mainly encaptured the trend of the patient's vitals and the frequency with which the doctor is taking the tests. Some of our features were :-
#
1) The parameters of the cubic fit of the vitals data(after it had been cleaned and it's moving avg. taken). The polynomial regression of the vital parameters allowed us to determine the trend of the vitals. We noticed that a constantly decreasing BP meant that the patient was likely to die.
#
2) The difference of timestamps ie. the frequency with which the patient as the more frequently the patient's vitals are checked => the more serious he is(the doctor knows best).
#
3) The min, max and the std. deviation of the vitals wrt. the normal values. The moving std. deviation was a good measure to determine how much the values differed from normal value.
#
Our approach gave quite nice results for the validation data. We were in top 5 in it's rankings.
