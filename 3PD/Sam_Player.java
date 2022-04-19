/**
 # To be copied from ThreePrisonersDilemma.java after running the tournament
 # Filename    : Au_JitSeah_Player.java
 # Created by  : Au Jit Seah
 */


public class Sam_Player { // extends Player
    int selectAction(int n, int[] myHistory, int[] oppHistory1, int[] oppHistory2) {
        // Starts with cooperation
        if (n == 0)
            return 0;

        // Punish defection immediately gives a 25% boost and attempt to take extra bit of payoff
        if (oppHistory1[n-1] == 1 || oppHistory2[n-1] == 1 || n >= 109)
            return 1;

        // Both opponents previous round is the same, choose action like Tit-For-Tat; but not really useful
        // if (oppHistory1[n-1] == oppHistory2[n-1])
        //		return oppHistory1[n-1];

        // Attempt to reset to cooperation from previous defection; but not really useful
        // if (myHistory[n-1] == 1)
        //		return 0;

		//	int defect_threshold = 1;
		//	boolean cooperate = false;
		//	if (n > defect_threshold)
		//			for (int i = 0; i < defect_threshold; i++) {
		//				if (myHistory[n-(i+1)] == 0)
		//						cooperate = true;
		//			}

					// Try to cooperate if myHistory more than defect_threshold
		//			if (cooperate == false) {
		//				System.out.println("Reset to Cooperate after defect threshold");
		//				return 0;
		//			}

        // For odd rounds - play like the Tolerant player
        if (n % 2 != 0) {
            int opponentCoop = 0;
            int opponentDefect = 0;

            for (int i = 0; i < n; i++) {
                if (oppHistory1[i] == 0)
                    opponentCoop += 1;
                else
                    opponentDefect += 1;

                if (oppHistory2[i] == 0)
                    opponentCoop += 1;
                else
                    opponentDefect += 1;
            }

            // Choose to only defects if at least half of the other players' actions have been defects
            return (opponentDefect > opponentCoop) ? 1 : 0;
        }


        // For even rounds - check history of defections - GuiltyPlayer
        int myNumDefections = 0;
        int oppNumDefections1 = 0;
        int oppNumDefections2 = 0;

        // Checks the total number of defections for both opponents and oneself
        for (int index = 0; index < n; ++index) {
            myNumDefections += myHistory[index];
            oppNumDefections1 += oppHistory1[index];
            oppNumDefections2 += oppHistory2[index];
        }

        // Player has greater or equal no. of defections than both opponents, player should be nice and cooperate
        // || does not make substantial differences
        if (myNumDefections >= oppNumDefections1 && myNumDefections >= oppNumDefections2)
            // Cooperates whenever possible : ranking is around 513-613
            return 0;
        else
            // Defects make ranking suffers greatly (approx. 10)
            return 1;
    }
}