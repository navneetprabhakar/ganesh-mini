#[path = "solution.rs"]
mod solution;

#[test]
fn all_u8_positions_match_independent_bottom_up_action_oracle() {
    // Internal score scale mirrors the reference only to express the specified
    // faster-win/slower-loss ordering; assertions do not prescribe its scale.
    let mut scores = vec![-1000i16; 256];
    let mut actions = vec![0u8; 256];
    for n in 1usize..256 {
        let mut best = i16::MIN;
        for amount in 1..=n.min(2) {
            let child = -scores[n - amount];
            let score = if child > 0 { child - 1 } else { child + 1 };
            if score > best {
                best = score;
                actions[n] = amount as u8;
            }
        }
        scores[n] = best;
    }
    for tokens in 0u8..=255 {
        for first_players_turn in [false, true] {
            let found = solution::solve(solution::GameState { tokens, first_players_turn });
            let expected = if tokens == 0 { None } else { Some(actions[tokens as usize]) };
            assert_eq!(found.action.map(|a| a.0), expected, "tokens={tokens}, turn={first_players_turn}");
            assert_eq!(found.score.signum(), scores[tokens as usize].signum(), "tokens={tokens}");
        }
    }
}
