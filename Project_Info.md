# Cognida – Project-1 – AI Powered Software Engineering Agent
 
## Description:
This project basically connects your application to the GitHub. It goes through the codebases, understands the project and its structure and finds bugs. It also recommends few solutions and generates code changes, allows you to run tests. It essentially acts as a smaller version of GitHub copilot, but it focuses on autonomous repository analysis and verified code fixes.
 
## Example Problem Statement:
Consider a company with a project containing a large number of files, and its discovered that login page is failing. Normally, a developer has to examine multiple files in order to identify the bug, but here our agent identifies the bug for us and also provides us with possible solutions along with running tests and creating PR.

## General Structure:
It has 5 main interfaces essentially, they are:
1. 	Repository Dashboard: Users can connect with their GitHub, select repositories, view branches, see previous agent tasks, and start code analysis.
2. 	AI Agent Workspace: Users can ask questions regarding any git related issues and the agent provides with solutions.
3. 	Code Review Interface: Shows original code, proposed modifications, effected files and explanations.
4. 	Testing Dashboard: It undergoes multiple tests to check for any issues, and displays tests that have been passed, tests that have been failed and any warnings.
5. 	Agent Performance Dashboard: Tracks successful bug fixes, failed attempts, test coverage changes, average execution time, token usage and cost.

## Workflow:
 ```mermaid
flowchart TD
    A["User Login"]
    B["GitHub Connection"]
    C["User Submits a Task"]
    D["AI Code Analysis"]
    E["Root Cause Identification"]
    F["Generates Code and Runs Tests"]
    G["Creates a GitHub PR"]
    H["Human-in-the-Loop"]
    I["Results and Analysis"]

    A --> B
    B --> C
    C --> D
    D --> E
    E --> F
    F --> G
    G --> H
    H --> I
```


