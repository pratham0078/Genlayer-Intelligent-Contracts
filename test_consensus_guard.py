"""
Direct-mode tests using the official GenLayer testing conventions.

Run with the GenLayer project toolchain installed. These tests have not been
executed in the package-generation environment.
"""
import json
import pytest


def test_initial_state(direct_deploy):
    contract = direct_deploy("contracts/consensus_guard.py", "The deliverable must include a README, tests, and deployment instructions.")
    case = json.loads(contract.get_case())
    assert case["status"] == "OPEN"
    assert case["verdict"] == "UNREVIEWED"
    assert case["evidence_submitted"] is False
    assert case["evidence_version"] == 0


def test_rejects_short_criteria(direct_deploy, direct_vm):
    with direct_vm.expect_revert("Acceptance criteria must be at least 20 characters."):
        direct_deploy("contracts/consensus_guard.py", "too short")


def test_rejects_evidence_before_submission(direct_deploy, direct_vm):
    contract = direct_deploy("contracts/consensus_guard.py", "The deliverable must include a README, tests, and deployment instructions.")
    with direct_vm.expect_revert("Submit evidence before adjudication."):
        contract.adjudicate()


def test_submit_evidence_updates_state(direct_deploy):
    contract = direct_deploy("contracts/consensus_guard.py", "The deliverable must include a README, tests, and deployment instructions.")
    contract.submit_evidence(
        "vendor",
        "The repository includes README.md, tests/, and deployment instructions in the README."
    )
    case = json.loads(contract.get_case())
    assert case["status"] == "EVIDENCE_SUBMITTED"
    assert case["submitter_label"] == "vendor"
    assert case["evidence_submitted"] is True
    assert case["evidence_version"] == 1


def test_evidence_can_be_replaced_before_resolution(direct_deploy):
    contract = direct_deploy("contracts/consensus_guard.py", "The deliverable must include a README, tests, and deployment instructions.")
    contract.submit_evidence("vendor", "Initial evidence package contains a short project overview.")
    contract.submit_evidence("vendor", "Updated evidence includes README.md, tests/, and deployment instructions.")
    case = json.loads(contract.get_case())
    assert case["evidence_version"] == 2
    assert case["status"] == "EVIDENCE_SUBMITTED"


def test_rejects_too_short_evidence(direct_deploy, direct_vm):
    contract = direct_deploy("contracts/consensus_guard.py", "The deliverable must include a README, tests, and deployment instructions.")
    with direct_vm.expect_revert("Evidence must be at least 20 characters."):
        contract.submit_evidence("vendor", "short")
