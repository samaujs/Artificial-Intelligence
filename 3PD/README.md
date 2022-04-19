## MultiAgent Systems (Self-Interested agents)
### 3 players Infinite Prisoner’s Dilemma (3p-IPD) game
> - For the 3 players Prisoner’s Dilemma game (3p-PD), the dominant defection strategy relies on the fact that it is a one shot game with no future.

> - On the other hand, for the 3 players Infinite Prisoner’s Dilemma game (3p-IPD) whereby the three players may meet each other again.  This encourages the players to develop strategies based on the previous game interactions.  Thus, a player’s current move may affect how his/her opponents behave in the future and affect the player’s future payoffs.

> - This apparently helps to remove the single dominant strategy of defection because the players can use more complex strategies dependent on game history to maximise the payoffs they will receive.

> - The players Pay-offs matrix is :
![alt text](https://github.com/samaujs/Artificial-Intelligence/blob/main/3PD/Pay-offs%20Matrix.png?raw=true)

### Definitions and Observations :

> - Let D and C to represent Defection (1) and Cooperation (0) respectively
> - Assume a symmetric game matrix, XCD could be written as XDC, where X may be C or D
> - U(DCC) > U(CCC) > U(DCD) > U(CCD) > U(DDD) > U(CDD)
> - D is the dominant strategy for any player

### The commom complex player strategies are :

> 1. **NicePlayer** : Always cooperate.
> 2. **NastyPlayer** : Always defect.
> 3. **RandomPlayer** : Cannot make up one’s mind, cooperates and defects randomly.
> 4. **TolerantPlayer** : Only defects if at least half of the other players' actions have been defects.
> 5. **FreakyPlayer** : Determines at the start of the match randomly to be nice or nasty at all times.
> 6. **T4TPlayer** : Picks a random opponent at each play and uses the 'tit-for-tat' strategy against them.

### New proposed player strategy with the following characteristics :
> 1. **Play nice** : Always be nice and starts with cooperation.
> 2. **Fast to anger** : Plays immediate defection when one of its two opponents plays defection.
> 3. **Forgiving** : Does not hold grudges and seek for cooperation.
> 4. **Reconciliation** : After player defects, player checks predefined observation rounds from history and attempts to reconcile defections with future cooperations.  If both opponents want to cooperate during these observation rounds, player will play nice immediately with cooperation.  The player will also cooperate for at least one more round (configurable) to show good will of cooperation.
> 5. **Cunning** : Plays defection with attempt to take extra bit of payoff for rounds greater than 109 (last round if there are 110 rounds).

## Run the code :
```
> javac ThreePrisonersDilemma.java
> java ThreePrisonersDilemma
```

## References :<br>
>[1] Chapter 11 “An Introduction to MultiAgent Systems, second edition” by Micheal Woolridge, 2012<br>
>[2] Iterated symmetric three-player prisoner’s dilemma game by Essam El-Seidy and Karim.M. Soliman<br>
>[3] [Game Theory, Axelrod’s Tournament by Janet Chen, Su-I Lu and Dan Vekhter](https://cs.stanford.edu/people/eroberts/courses/soco/projects/1998-99/game-theory/axelrod.html)<br>
>[4] [The Three-Player Prisoner's Dilemma by Computer Science University of Chicago](https://www.classes.cs.uchicago.edu/archive/1998/fall/CS105/Project/node6.html)<br>
>[5] Reinforcement Learning: An Introduction second edition, by Richard S. Sutton and Andrew G. Barto, 2018.<br>
