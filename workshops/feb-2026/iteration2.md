# Iteration 2 — Expert-Guided AI Application Prompt

## Purpose
This prompt demonstrates how **human expertise dramatically improves AI-generated infrastructure**
by adding guardrails, reducing blast radius, and controlling cost — without changing the application itself.

The goal is to show that:
> AI speed + human judgment = production-ready systems

---

## Prompt

You are an AWS **solutions architect** designing production-ready infrastructure.

Take the previously generated Terraform application (public API with Lambda and DynamoDB) and **refactor it** according to the following **expert constraints**.

---

### 1. IAM & Security Guardrails
- All workload IAM roles (Lambda execution role, deployment roles) **must use an IAM Permission Boundary**
- Permission boundary must:
  - Prevent privilege escalation
  - Disallow wildcard access to IAM, KMS, and AWS Organizations
- Lambda execution role must follow **least privilege**:
  - Only required DynamoDB actions
  - Permissions scoped to the specific DynamoDB table ARN

---

### 2. Network Isolation
- Lambda must run inside a **VPC**
- Use **private subnets only** (no public IPs)
- Do **not** use a NAT Gateway unless strictly required
- Use a **DynamoDB VPC Gateway Endpoint** so traffic stays inside AWS
- Security groups must be explicit and restrictive

---

### 3. Cost Controls & Predictability
- Set CloudWatch log retention to **14 days**
- Configure **Lambda reserved concurrency** to limit runaway scaling
- Enable **API Gateway throttling**
- Add:
  - AWS Budget (monthly)
  - Budget notifications
  - CloudWatch alarms for:
    - Lambda errors
    - API Gateway 5XX errors

---

### 4. Operational Hygiene
- Add consistent tags to all resources:
  - `owner`
  - `environment`
  - `cost-center`
- Separate Terraform logically:
  - Networking
  - IAM
  - Application
- Prefer safe-by-default design over convenience

---

### Output Requirements
- Terraform code only
- Clear structure and comments explaining *why* decisions were made
- Assume this will be used by a real engineering team in a real company

Optimize for **security, blast-radius reduction, and cost safety**, not speed.

---

## Key Message for the Workshop
The application did not change.
The **human framing** did.
