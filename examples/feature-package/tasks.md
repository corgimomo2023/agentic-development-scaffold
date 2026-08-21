# Example: Project Health Command Tasks

## TASK-001: Propagate validator failure

- Test first: create a subprocess test with a controlled failing validator.
- RED: run the focused test and verify the command does not exist.
- GREEN: add the minimal command wrapper.
- Verify: focused test, then full suite.
- Review: independent spec review, then quality review.

## TASK-002: Run tests after validator success

Repeat RED-GREEN-REFACTOR for test-runner invocation and exit-code propagation.
