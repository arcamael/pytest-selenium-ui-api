# Test Strategy & Recommendations

## Tests choice
`test_place_single_bet_happy_path()` - Placing a single bet is the product's core revenue journey and
the highest-value thing to protect. It exercises the full money chain in one
flow — match selection, stake entry, live payout computation, placement, the
success receipt, and the resulting balance change.

`test_invalid_stake_is_rejected()` - Single parametrized test_invalid_stake_is_rejected() verifies boundary values, equivalence
partitioning, and type checks for the `stake` field. This allows to cover a range of regression risks
for a critical field in the /place-bet API endpoint.


## Top recommendations if this project were to scale, in priority order.

### 1. Specification improvements

Consider improving tech specification on following (most critical):
1. Let's have a single place in the doc for each requirement, so they don't repeat. It will fix ambiguity and increase manageability of reqs.
2. Assign ID to every atomic requirement so we can trace its implementation and testing further.
3. Prioritise adding capabilities for API (primary) and UI of placed Bets management (`GET /bets` endpoint for example would add much value). Feature is Bet Placement but results are not manageable unless there is a direct access to DB holding Bets.

Reasoning: Well-structured PRD allows to identify bugs on this stage better. Precise treceability is a huge quality booster.

### 2. Testing

General consideration: since product is in early phase of development investing in deep coverage with UI and API autotest is not reasonable since both will change dramatically. So apart from manual testing of feature increments and adding reasonable autotesting coverage for regression verifications it worth to invest in:


1. Excell test failures reporting.
2. Prepare code structure for further API contract testing so that it's fast to implement once major API gaps are fixed and it is stable enough to take a snaphot of the current state.
3. Implement AI agents for analysing/clustering CI failures (potential bug vs valid update of UI/API) and test auto healing capabilities. Don't inject them into regular CI pipeline for now to avoid redundant budgeting but be ready for scaling.
4. Same for AI agents on PR review with breaking changes analysis and trecability between PR changes and PRD, which allow to run selective test scope.
