// ** added for saving results to file output **
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;

public class ThreePrisonersDilemma {
	
	/* 
	 This Java program models the two-player Prisoner's Dilemma game.
	 We use the integer "0" to represent cooperation, and "1" to represent 
	 defection. 
	 
	 Recall that in the 2-players dilemma, U(DC) > U(CC) > U(DD) > U(CD), where
	 we give the payoff for the first player in the list. We want the three-player game 
	 to resemble the 2-player game whenever one player's response is fixed, and we
	 also want symmetry, so U(CCD) = U(CDC) etc. This gives the unique ordering
	 
	 U(DCC) > U(CCC) > U(DDC) > U(CDC) > U(DDD) > U(CDD)
	 
	 The payoffs for player 1 are given by the following matrix: */


	static int[][][] payoff = {
		{{6,3},  //payoffs when first and second players cooperate 
		 {3,0}}, //payoffs when first player coops, second defects
		{{8,5},  //payoffs when first player defects, second coops
	     {5,2}}};//payoffs when first and second players defect
	
	/* 
	 So payoff[i][j][k] represents the payoff to player 1 when the first
	 player's action is i, the second player's action is j, and the
	 third player's action is k.
	 
	 In this simulation, triples of players will play each other repeatedly in a
	 'match'. A match consists of about 100 rounds, and your score from that match
	 is the average of the payoffs from each round of that match. For each round, your
	 strategy is given a list of the previous plays (so you can remember what your 
	 opponent did) and must compute the next action.  */
	
	
	abstract class Player {
		// This procedure takes in the number of rounds elapsed so far (n), and 
		// the previous plays in the match, and returns the appropriate action.
		int selectAction(int n, int[] myHistory, int[] oppHistory1, int[] oppHistory2) {
			throw new RuntimeException("You need to override the selectAction method.");
		}
		
		// Used to extract the name of this player class.
		final String name() {
			String result = getClass().getName();
			return result.substring(result.indexOf('$')+1);
		}
	}
	
	/* Here are four simple strategies: */
	
	class NicePlayer extends Player {
		//NicePlayer always cooperates
		int selectAction(int n, int[] myHistory, int[] oppHistory1, int[] oppHistory2) {
			return 0; 
		}
	}
	
	class NastyPlayer extends Player {
		//NastyPlayer always defects
		int selectAction(int n, int[] myHistory, int[] oppHistory1, int[] oppHistory2) {
			return 1; 
		}
	}
	
	class RandomPlayer extends Player {
		//RandomPlayer randomly picks his action each time
		int selectAction(int n, int[] myHistory, int[] oppHistory1, int[] oppHistory2) {
			if (Math.random() < 0.5)
				return 0;  //cooperates half the time
			else
				return 1;  //defects half the time
		}
	}
	
	class TolerantPlayer extends Player {
		//TolerantPlayer looks at his opponents' histories, and only defects
		//if at least half of the other players' actions have been defects
		int selectAction(int n, int[] myHistory, int[] oppHistory1, int[] oppHistory2) {
			int opponentCoop = 0;
			int opponentDefect = 0;
			for (int i=0; i<n; i++) {
				if (oppHistory1[i] == 0)
					opponentCoop = opponentCoop + 1;
				else
					opponentDefect = opponentDefect + 1;
			}
			for (int i=0; i<n; i++) {
				if (oppHistory2[i] == 0)
					opponentCoop = opponentCoop + 1;
				else
					opponentDefect = opponentDefect + 1;
			}
			if (opponentDefect > opponentCoop)
				return 1;
			else
				return 0;
		}
	}
	
	class FreakyPlayer extends Player {
		//FreakyPlayer determines, at the start of the match, 
		//either to always be nice or always be nasty. 
		//Note that this class has a non-trivial constructor.
		int action;
		FreakyPlayer() {
			if (Math.random() < 0.5)
				action = 0;  //cooperates half the time
			else
				action = 1;  //defects half the time
		}
		
		int selectAction(int n, int[] myHistory, int[] oppHistory1, int[] oppHistory2) {
			return action;
		}	
	}

	class T4TPlayer extends Player {
		//Picks a random opponent at each play, 
		//and uses the 'tit-for-tat' strategy against them 
		int selectAction(int n, int[] myHistory, int[] oppHistory1, int[] oppHistory2) {
			if (n==0) return 0; //cooperate by default
			if (Math.random() < 0.5)
				return oppHistory1[n-1];
			else
				return oppHistory2[n-1];
		}	
	}

	// ** added a new player strategy **
	class Sam_Player extends Player {
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

	/* In our tournament, each pair of strategies will play one match against each other. 
	 This procedure simulates a single match and returns the scores. */
	float[] scoresOfMatch(Player A, Player B, Player C, int rounds) {
		int[] HistoryA = new int[0], HistoryB = new int[0], HistoryC = new int[0];
		float ScoreA = 0, ScoreB = 0, ScoreC = 0;
		
		for (int i=0; i<rounds; i++) {
			int PlayA = A.selectAction(i, HistoryA, HistoryB, HistoryC);
			int PlayB = B.selectAction(i, HistoryB, HistoryC, HistoryA);
			int PlayC = C.selectAction(i, HistoryC, HistoryA, HistoryB);
			ScoreA = ScoreA + payoff[PlayA][PlayB][PlayC];
			ScoreB = ScoreB + payoff[PlayB][PlayC][PlayA];
			ScoreC = ScoreC + payoff[PlayC][PlayA][PlayB];
			HistoryA = extendIntArray(HistoryA, PlayA);
			HistoryB = extendIntArray(HistoryB, PlayB);
			HistoryC = extendIntArray(HistoryC, PlayC);
		}
		float[] result = {ScoreA/rounds, ScoreB/rounds, ScoreC/rounds};
		return result;
	}
	
//	This is a helper function needed by scoresOfMatch.
	int[] extendIntArray(int[] arr, int next) {
		int[] result = new int[arr.length+1];
		for (int i=0; i<arr.length; i++) {
			result[i] = arr[i];
		}
		result[result.length-1] = next;
		return result;
	}
	
	/* The procedure makePlayer is used to reset each of the Players 
	 (strategies) in between matches. When you add your own strategy,
	 you will need to add a new entry to makePlayer, and change numPlayers.*/
	
	int numPlayers = 7;  // default is 6
	Player makePlayer(int which) {
		switch (which) {
		case 0: return new NicePlayer();
		case 1: return new NastyPlayer();
		case 2: return new RandomPlayer();
		case 3: return new TolerantPlayer();
		case 4: return new FreakyPlayer();
		case 5: return new T4TPlayer();

		// ** added new player strategy **
		case 6: return new Sam_Player();
		}
		throw new RuntimeException("Bad argument passed to makePlayer");
	}
	
	/* Finally, the remaining code actually runs the tournament. */

	// ** added to run tournament x times to obtain the ranking statistics **
	private int numOfTournaments = 1000;

	public static void main (String[] args) {
		ThreePrisonersDilemma instance = new ThreePrisonersDilemma();

		// ** added for storing player total scores **
		ArrayList<Double>[] players_scores = new ArrayList[instance.numPlayers];
		// players_rank_counts = [2, 0, 0, 0, 1, 0]; counts of 2 with first rank position at index 0
		ArrayList<Integer>[] players_rank_counts = new ArrayList[instance.numPlayers];

		// Array of ArrayList
		for (int i = 0; i < instance.numPlayers; i++) {
			players_scores[i] = new ArrayList<Double>();
			players_rank_counts[i] = new ArrayList<Integer>();

			// Initialise the respective rank counts for a player
			for (int j = 0; j < instance.numPlayers; j++)
				players_rank_counts[i].add(0);
		}

		for (int i=0; i<instance.numOfTournaments; i++) {
			System.out.println("Tournament " + (i+1) + " :");
			System.out.println("------------------------------------------------------------------------");
			// Run tournaments to evaluate the performance of individual strategy based on average ranking
			instance.runTournament(players_scores, players_rank_counts);
			System.out.println("-------------------------------------------------------------------------------------");
		}

		// Check for all stored total scores for each tournament run
		for (int i=0; i<instance.numPlayers; i++) {
			System.out.println(instance.makePlayer(i).name() +
							   " with scores : " + players_scores[i] +
							   " with rank_counts : " + players_rank_counts[i]);
		}

		// Storing all total scores for performance analysis
		instance.FileOutput(players_scores, "./3PD_TotalScores.csv", 1);
		instance.FileOutput(players_rank_counts, "./3PD_RankCounts.csv", 2);
	}

	boolean verbose = true;  // set verbose = false if you get too much text output

	// takes an argument on the number of rounds and player_scores
	void runTournament(ArrayList<Double>[] players_scores, ArrayList<Integer>[] players_rank_counts) {
		float[] totalScore = new float[numPlayers];

		// This loop plays each triple of players against each other.
		// Note that we include duplicates: two copies of your strategy will play once
		// against each other strategy, and three copies of your strategy will play once.

		// ** added to print playerCombination per Tournament **
		// when i = 0 : (7) + (6) + (5) + (4) + (3) + (2) + (1) = 28
		// when i = 1 : (6) + (5) + (4) + (3) + (2) + (1) = 21
		// when i = 2 : (5) + (4) + (3) + (2) + (1) = 15
		// when i = 3 : (4) + (3) + (2) + (1) = 10
		// when i = 4 : (3) + (2) + (1) = 6
		// when i = 5 : (2) + (1) = 3
		// when i = 6 : (1) = 1
		// Total playerCombination = 28 + 21 + 15 + 10 + 6 + 3 + 1 = 84 vs 56 games for 6 Players

		int playerCombination = 0;

		for (int i=0; i<numPlayers; i++) for (int j=i; j<numPlayers; j++) for (int k=j; k<numPlayers; k++) {

			Player A = makePlayer(i); // Create a fresh copy of each player
			Player B = makePlayer(j);
			Player C = makePlayer(k);
			int rounds = 90 + (int)Math.rint(20 * Math.random()); // Between 90 and 110 rounds
			float[] matchResults = scoresOfMatch(A, B, C, rounds); // Run match
			totalScore[i] = totalScore[i] + matchResults[0];
			totalScore[j] = totalScore[j] + matchResults[1];
			totalScore[k] = totalScore[k] + matchResults[2];
			if (verbose) {
				System.out.println(A.name() + " scored " + matchResults[0] +
						" points, " + B.name() + " scored " + matchResults[1] +
						" points, and " + C.name() + " scored " + matchResults[2] + " points.");

				// ** added to print total number of rounds **
				playerCombination ++;
				System.out.println("Player rounds : " + rounds + " and player combination no. : " + playerCombination);
				System.out.println("i : " + i + " j :" + j + " k :" + k);
				System.out.println("-------------------------------------------------------------------------------------");
			}

		}

		int[] sortedOrder = new int[numPlayers];
		// This loop sorts the players by their score.
		for (int i=0; i<numPlayers; i++) {
			int j=i-1;
			for (; j>=0; j--) {
				if (totalScore[i] > totalScore[sortedOrder[j]]) 
					sortedOrder[j+1] = sortedOrder[j];
				else break;
			}
			sortedOrder[j+1] = i;
		}

		// * added for storing total scores and rank counts of each player in a tournament run **
		for (int i=0; i<numPlayers; i++) {
			// Store of the scores for each player in each tournament
			players_scores[i].add((double) totalScore[i]);
			System.out.println(makePlayer(i).name() + " scores : " + players_scores[i]);

			// sortedOrder[0] stores the best player index in a tournament run based on the makePlayer sequence
			// Increment rank count per tournament run
			// Eg. sortedOrder[0] gives RandomPlayer with index 2
			int playerIndex = sortedOrder[i];
			int currentRankCountValue =  players_rank_counts[playerIndex].get(i);

			// Increment the rank counter for each player
			players_rank_counts[playerIndex].set(i, currentRankCountValue+1);
		}

		// Finally, print out the sorted results and included
		if (verbose) System.out.println();
			System.out.println("Tournament Results");

			// ** added to show the top 3 players **
			for (int i=0; i<3; i++) {
				System.out.println("The top " + (i+1)  + " player for this tournament : " +
								   makePlayer(sortedOrder[i]).name());
			}

			System.out.println("-------------------------------------------------------------------------------------");
			// ** modified the flow and added to show the player accumulated rank count details **
			for (int i=0; i<numPlayers; i++) {
				System.out.println(makePlayer(sortedOrder[i]).name() + ": " +
								   totalScore[sortedOrder[i]] + " points; with rank counts : " +
								   players_rank_counts[sortedOrder[i]]);
			}

	} // end of runTournament()

	// ** added for saving performance results that can be used for comparative analysis **
	public void FileOutput(ArrayList[] arrayListData, String filename, Integer type) {
		String Param1;
		String Param2 = null;
		String col_name = "Player_name";

		try{
			// Append to existing file use the parameter append = true
			FileWriter writer = new FileWriter(filename);

			writer.append(col_name);

			if (type == 1) {
				System.out.println("Saving total scores of all players in CSV file...");
				System.out.println("-------------------------------------------------");

				//  Save total scores for each player
				// Create the column names based on the number of rounds
				for (int i=0; i<numOfTournaments; i++) {
					col_name = "round_" + (i+1);
					writer.append(',');
					writer.append(col_name);
				}

				// Next line after column names
				writer.append("\n");

				for (int i=0; i<numPlayers; i++) {
					Param1 = makePlayer(i).name();
					writer.append(Param1);

					for (int j=0; j<arrayListData[i].size(); j++) {
						writer.append(',');

						// Round to 3 decimal places
						// Param2 = Double.toString(Math.round(arrayListData[i] * 1000.0) / 1000.0);
						Param2 = String.valueOf(arrayListData[i].get(j));
						writer.append(Param2);
						// System.out.println("Player_name : " + Param1 + " with score : " + Param2);
					}

					// New row after retrieving all the total score data in the array of a player
					writer.append("\n");
				}
			} else if (type == 2) {
				System.out.println("Saving rank counts of all players in CSV file...");
				System.out.println("------------------------------------------------");
				// Save rank counts for each player
				// Create the column names based on the ranks
				for (int i=0; i<numPlayers; i++) {
					col_name = "Rank_" + (i+1);
					writer.append(',');
					writer.append(col_name);
				}

				// Next line after column names
				writer.append("\n");

				for (int i=0; i<numPlayers; i++) {
					Param1 = makePlayer(i).name();
					writer.append(Param1);

					for (int j=0; j<arrayListData[i].size(); j++) {
						writer.append(',');

						// Get the rank counter for each player
						Param2 = String.valueOf(arrayListData[i].get(j));
						writer.append(Param2);
						// System.out.println("Player_name : " + Param1 + " with rank count : " + Param2);
					}

					// New row after retrieving all the rank data in the array of a player
					writer.append("\n");
				}
			} else {
				System.out.println("Please input the right category for saving!");
			}

			// Housekeeping
			writer.toString();
			writer.flush();
			writer.close();

		} catch(IOException ioException){
			System.out.println("Catch Error when instantiating FileWriter");
		}
	}
} // end of class PrisonersDilemma

