class Sam_Player extends Player {
    // Store the number of defects taken by opponents
    int opp1_defects = 0;
    int opp2_defects = 0;

    // Store the round number where agent retaliate against defects
    int retaliateAtRound = -1;

    // Observe this number of previous rounds to check if opponents want to cooperate
    int observationRounds = 3;
    // No. of rounds to reverse previous defection effects to encourage opponents to cooperate
    int reverseRounds = -2;

    int selectAction(int n, int[] myHistory, int[] oppHistory1, int[] oppHistory2) {
        // Record defection counts after first round
        if (n > 0) {
            opp1_defects += oppHistory1[n - 1];
            opp2_defects += oppHistory2[n - 1];
        }

        // Starts with cooperation
        if (n == 0) {  // n < observationRounds
            return 0;
        }

        // Loop rounds with cooperation whereby agent cooperates in hope to reverse the effects of retaliation
        // Nullify by cooperating to reverse effect with preset -(retaliateAtRound + 1) rounds
        // Showing good will with cooperation for at least one more round
        if (retaliateAtRound < -1) {
            retaliateAtRound += 1;

            // Resets the opponent defects when agent cooperates
            opp1_defects = 0;
            opp2_defects = 0;
            return 0;
        }

        // Check at round retaliated + observationRounds to measure if opponents like to cooperate
        if (retaliateAtRound > -1 && n == retaliateAtRound + observationRounds + 1) {
            // Store the number of cooperation during observationRounds
            int opp1_coop = 0;
            int opp2_coop = 0;

            for (int prevRound = 0; prevRound < observationRounds; prevRound++) {
                // Check if opponents want to cooperate in the observationRounds
                opp1_coop += oppHistory1[n - 1 - prevRound] == 0 ? 1 : 0;
                opp2_coop += oppHistory2[n - 1 - prevRound] == 0 ? 1 : 0;
            }

            // If both opponents wish to cooperate in the observationRounds and previous round
            // Agent will cooperate with opponents immediately
            if (opp1_coop > 1 && opp2_coop > 1 && (oppHistory1[n - 1] + oppHistory2[n - 1]) == 0) {
                // When retaliateAtRound is negative, player will cooperate with the count goes backwards from -2
                // -2 indicates 1 round where agent plays cooperation to reverse effect of defect
                // -5 indicates 4 rounds where agent plays cooperation to reverse effect
                retaliateAtRound = reverseRounds;  // default value -2

                // Resets the opponent defects when agent cooperates
                opp1_defects = 0;
                opp2_defects = 0;
                return 0;
            } else {
                // agent defects at round n when there are no intentions of cooperation in the observationRounds
                retaliateAtRound = n;
                return 1;
            }
        }

        // Plays defection immediately when one of the opponents defected and attempt to take extra bit of payoff
        if (opp1_defects + opp2_defects > 0 || n >= 109) {
            // Stores the round number when defected
            retaliateAtRound = n;
            return 1;
        }

        // Cooperation is the default action; be nice at all times
        return 0;
    }
} // In 1,000 Tournament runs, agent ranks around 613-678