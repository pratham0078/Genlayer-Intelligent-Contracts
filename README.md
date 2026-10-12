# ConsensusGuard

**A reusable evidence-based adjudication primitive for GenLayer Intelligent Contracts.**

ConsensusGuard turns an agreement's natural-language acceptance criteria and a submitted evidence bundle into a consensus-backed outcome: `ACCEPT`, `REJECT`, or `INCONCLUSIVE`.

It is intended for software delivery, freelance milestones, bounties, grant deliverables, content licensing checks, and other workflows where evidence must be evaluated against criteria that are agreed in advance.

## Why this is more than an LLM wrapper

- **Criteria are fixed at deployment.** The contract stores the agreement's acceptance criteria before evidence is submitted.
- **Evidence is treated as untrusted input.** The adjudication prompt explicitly instructs reviewers to ignore embedded attempts to change the rules.
- **Validators independently reassess the evidence.** The leader proposes a structured result; validators rerun the assessment and require the same verdict plus a score difference of no more than 15 points.
- **Ambiguity is a first-class result.** Insufficient evidence can produce `INCONCLUSIVE` instead of forcing a binary decision.
- **State changes happen after consensus.** The contract writes the verdict, score, and rationale only after the nondeterministic call returns.
- **A case has a clear lifecycle.** `OPEN` → `EVIDENCE_SUBMITTED` → `RESOLVED`. Evidence can be updated before resolution; a resolved case is immutable.

## How consensus is used

`adjudicate()` calls `gl.vm.run_nondet_unsafe(leader_fn, validator_fn)`, following GenLayer's documented custom validator pattern.

1. The leader evaluates the criteria and evidence and returns a JSON decision.
2. Each validator independently repeats the assessment.
3. The validator checks that the proposed output is well-formed, its verdict is allowed, its score is between 0 and 100, the independent verdict matches, and the two scores differ by no more than 15.
4. Only the consensus-agreed result is parsed in deterministic context and written to contract state.

This is not a guarantee that the underlying evidence is true. Consensus establishes agreement on an evaluation under the contract's rules; it cannot make false evidence true. For high-value disputes, include independently verifiable URLs, content hashes, signed records, and human appeal procedures.

Official references:
- [GenLayer Intelligent Contracts: first contract](https://docs.genlayer.com/developers/intelligent-contracts/first-contract)
- [GenLayer non-determinism and custom validators](https://docs.genlayer.com/developers/intelligent-contracts/features/non-determinism)
- [GenLayer project boilerplate and testing workflow](https://github.com/genlayerlabs/genlayer-project-boilerplate)

## Repository layout

```text
consensusguard/
├── contracts/
│   └── consensus_guard.py
├── tests/
│   └── direct/
│       └── test_consensus_guard.py
├── examples/
│   └── sample_case.md
├── README.md
├── SECURITY.md
└── .gitignore
```

## Contract interface

### Constructor

`ConsensusGuard(acceptance_criteria: str)`

Deploy one instance per agreement. Criteria must be 20–4,000 characters.

### `submit_evidence(submitter_label, evidence)`

Submits or replaces evidence before resolution. Evidence must be 20–8,000 characters. The label is informational only and does not authenticate a person or organization.

### `adjudicate()`

Runs validator consensus and resolves the case. Call only after evidence has been submitted. The transaction can be expensive and slower than deterministic calls because validators perform independent nondeterministic work.

### `get_case()`

Returns JSON text containing criteria, current status, verdict, score, rationale, evidence version, and whether evidence has been submitted. The raw evidence is intentionally not included in this view response.

## Quick start

1. Create a project using the current [official GenLayer project boilerplate](https://github.com/genlayerlabs/genlayer-project-boilerplate) or the current GenLayer CLI workflow.
2. Copy `contracts/consensus_guard.py` into that project's `contracts/` directory.
3. Copy the direct tests into the project's `tests/direct/` directory and adapt only if the installed toolchain's fixtures or CLI have changed.
4. Run the project's linter and direct tests.
5. Deploy through GenLayer Studio or the CLI using the documented workflow for your installed version.
6. Use the constructor with clear criteria, call `submit_evidence`, then `adjudicate`, and inspect `get_case` after finality.

Suggested checks (exact commands depend on the currently installed CLI/toolchain):

```bash
genvm-lint check contracts/consensus_guard.py
pytest tests/direct/ -v
```

The tests in this repository are starter direct-mode tests written to the conventions documented in GenLayer's project boilerplate. **They have not been run here and are not represented as passing.** Confirm the fixtures and commands against the version of the official toolchain you install.

## Example

See [`examples/sample_case.md`](examples/sample_case.md) for a sample software-delivery acceptance case.

## Important limitations

- This first version is a single-agreement contract. Deploy one instance per agreement.
- `submitter_label` is not a verified identity, and this contract does not escrow or transfer funds.
- The contract evaluates evidence text supplied to it; it does not automatically fetch or verify URLs.
- Validators can agree on an incorrect result. Use clear criteria, evidence with provenance, and an appeal or human-review path for consequential disputes.
- Prompt injection defenses reduce risk but do not eliminate it.
- Do not use as the sole authority for legal, medical, safety-critical, or high-value financial decisions.
- Before mainnet use, review current GenVM syntax, limits, fees, storage behavior, and toolchain compatibility; run linting, direct tests, and Studio integration tests.

## License

MIT. See [`LICENSE`](LICENSE).
