# Reinforcement Learning (Dynamic Programming)
> Markov Decision Process with
>
>    - states, s
>    - actions, a
>    - Transition model, P(s'|s,a)
>    - Reward function, R(s)
>    - Discount factor, γ

>(A) Value Iteration
- Bellman equation, ***U_i+1(s) = R(s) + γ max a∈A(s) ∑s′ P(s′|s,a) U_i(s′)***
- Maximum error allowed in the utility of any state, ε
- For different values of c in ε = c · Rmax,
    - we can use c to control the number of value iterations k required to guarantee an error of at most ε
- Termination criteria, the maximum change in the utility of any state in an iteration, δ < ϵ(1−γ)/γ

>(B) Policy Iteration
- Policy Evaluation
    - ***U_i+1(s) ← R(s) + γ ∑s′ P(s'|s, π_i(s)) U_i(s')***
- Policy Improvement
    - if max a∈A(s) ∑s′ P(s'|s, a) U_π_i(s') > ∑s′ P(s'|s, π[s]) U(s') then update the best policy
    - ***π_i+1(s) = max a∈A(s) ∑s′ P(s'|s, a) U_π_i(s')***
- Termination criteria, policy π remains unchanged for all states from previous iteration

>(C) Modified Policy Iteration
- Policy Evaluation
    - ***U_i+1(s) ← R(s) + γ ∑s′ P(s'|s, π_i(s)) U_i(s')***, repeat k times to produce the next utility estimate
    - k number of simplified value iteration steps (with fixed policy, π_i)
    - these utility estimates give reasonably good approximation of the utilities.
- Policy Improvement
    - if max a∈A(s) ∑s′ P(s'|s, a) U_π_i(s') > ∑s′ P(s'|s, π[s]) U(s') then update the best policy
    - ***π_i+1(s) ← max a∈A(s) ∑s′ P(s′|s, a) U_i+k_π_i(s′)***
- Termination criteria, policy π remains unchanged for all states from previous iteration
- This is often much more efficient than standard Policy Iteration or Value Iteration.<br><br>


> References :<br>
[1] Chapters 16 & 17 “Artificial Intelligence: A Modern Approach” by S. Russell and P. Norvig. Prentice-Hall, third edition, 2010<br>
[2] Reinforcement Learning: An Introduction second edition, by Richard S. Sutton and Andrew G. Barto, 2018.<br>
