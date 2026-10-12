# Security considerations

- Treat evidence as adversarial user input; do not include secrets in evidence.
- The contract's prompt instructs validators to ignore embedded instructions, but prompt injection is not fully preventable.
- Acceptance criteria should be specific, measurable, and agreed before evidence submission.
- The submitter label is not authentication.
- This version has no escrow, payment release, identity verification, or external URL verification.
- Use independent evidence such as signed records, hashes, and trusted artifact links for consequential disputes.
- A consensus result is an agreed adjudication, not a cryptographic proof that the evidence is true.
- Test the deployed version in a safe environment before relying on it.
