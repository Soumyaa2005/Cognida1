# Weekly Report – Week 3

- **Name:** Vemuri Sai Soumya
- **Role:** Intern
- **Mentor:** Sai Kumar Yerra

## 1. Brief Summary

This week, I mainly worked on understanding how the Code Quality Rules Engine can be built for Rino.

- Explored software principles like SOLID, DRY, and KISS.
- Looked into code quality, design quality, and architectural review.
- Researched tools like Trivy, Ruff, ESLint, and pytest.
- Explored ways to detect vulnerable packages and other security issues.
- Worked on understanding how YAML rules can be connected to a Python script.
- Started planning how the script can analyze a repository and list the issues it finds.
- Explored how an LLM can be used along with deterministic checks.

## 2. Tasks Completed

- **Code Quality Rules Engine:** Started exploring how Rino can check a repository for code quality issues using predefined rules.

- **Software Principles:** Went through SOLID principles, DRY, and KISS to understand how they help make code easier to maintain, read, and extend.

- **Clean Code:** Looked into practices such as using meaningful names, writing simple and readable code, avoiding repetition, and keeping code modular.

- **VAPT Tools:** Researched tools like Trivy, Renovate, and Dependabot to understand how they can help identify vulnerable packages and dependencies.

- **Code Analysis Tools:** Explored Ruff and ESLint for checking code quality and identifying common issues in Python and JavaScript/TypeScript code.

- **Testing:** Looked into pytest and explored how existing tests can be used to validate code, along with identifying areas where testing is missing.

- **Execution Environment:** Explored different ways to run the analysis, including development instances, GitHub Actions, and Rino's own sandbox. Also looked into the tradeoffs of each approach.

- **Rule Configuration:** Worked on understanding how rules can be defined in YAML and how the Python script can read those rules and run the corresponding checks.

- **System Prompt:** Started outlining what instructions would be needed for the LLM to analyze and explain code quality issues.

- The idea is to have the script analyze the repository and provide an output listing the code quality and security issues it identifies.

## 3. Key Outcomes

- Got a clearer idea of what the Code Quality Rules Engine should check.
- Understood how deterministic checks and LLM-based analysis can work together.
- Identified open-source tools that can be used for code quality and security checks.
- Outlined the initial structure of the rule files and analysis script.
- Planned how to test the rules on an existing repository and generate an issue report.
