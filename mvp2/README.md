# MVP 2: Optimizing Election Campaigning Strategy by Locating Persuadable Voters

## Problem
In recent presidential elections, the majority of voters know whom they will vote for months in advance. It is therefore a waste of time and money for candidates to try and persuade these voters to their side. The goal of this project is to find locations where there are many people who are more likely to be persuaded one way or another - people who are open to voting for either candidate. These are the voters that candidates need to reach out to in order to win the election.

## Solution
The robust solution would take into account split ballots (e.g. someone voting for the Republican Presidential candidate but a Democratic Representative for Congress), the total population of voting precincts, the percentage of voters who are registered for a party vs. those who are not registered, and other factors. The solution would combine all these variables to find locations where presidential candidates should spend the most amount of their time campaigning because these locations would contain the largest number of voters who are able to be persuaded to vote for the candidate.

## Challenges
1. Logistical: It will be logistically difficult to standardize data across the entire U.S. Because elections are run at the state level, there could potentially be 50 different data formats to combine. Additionally, it is common for precinct boundaries to change from one election to the next, so it may or may not be possible to directly compare results from two different elections. 
2. Specificity: Because individual ballots are anonymized (which is a very good thing), the program would only be able to tell candidates general locations where they should be campaigning; it would not be able to say, “Go talk to John Doe who lives on 123 Main Street because he is likely to be receptive to your message.”

## My MVP
This MVP will identify precincts in Minnesota where there are relatively large numbers of 'split ticket' ballots. That is, ballots where a voter might have chosen a Republican candidate for president but a Democratic candidate for U.S. House. People who split their ballot are less loyal to a particular party, so they would therefore be more likely to change their mind to support or oppose a political candidate based on that candidate's campaign. These 'split ticket' voters are people whom candidates should target because they are key to winning an election.

## The Program
`mvp2.ipynb` features all the code for this MVP.\
The program first reads in a GeoJSON file containing precinct boundaries in Minnesota. This file is converted into a GeoPandas GeoDataFrame. Next, precinct-level results from the 2020 presidential, Senate, and House elections are added to this GeoDataFrame. Then, the program searches for precincts that have a relative high percentage of split ballots. Finally, the program finds which counties have the highest population of voters who live in precincts that have a high percentage of split ballots.