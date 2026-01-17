# Iteration 1 — Naive AI Application Prompt

## Purpose
This prompt intentionally produces a **working but unsafe and ungoverned AWS setup**.
It represents what happens when AI is asked to “just make it work” without expert framing.

This is the **baseline** used in the workshop to demonstrate common pitfalls:
- Over-permissioned IAM
- Public-by-default networking
- No cost controls
- No guardrails

---

## Prompt

You are an AWS cloud engineer.

Generate **Terraform** code to deploy a simple backend application in AWS with the following requirements:

### Application
- A public REST API
- API Gateway REST API
- AWS Lambda (Python) as backend
- DynamoDB table to store “orders”
- Two endpoints:
  - `POST /orders` → create order
  - `GET /orders/{id}` → fetch order

### Infrastructure
- Everything should be deployable in one AWS account
- The API must be publicly accessible from the internet
- Include CloudWatch logging
- Keep the solution simple and easy to understand

### Constraints
- Do not over-engineer
- Focus on making it work end-to-end

### Output requirements
- Terraform code only
- All resources in a single configuration
- Assume default AWS settings where possible

---

## Expected Characteristics (Do Not Fix)
- Broad IAM permissions
- Public access without strong boundaries
- Minimal or no network isolation
- No cost or usage controls
- No explicit governance decisions
