# Weekly Report – Week 2

- **Name:** Vemuri Sai Soumya
- **Role:** Intern
- **Mentor:** Sai Kumar Yerra

## 1. Brief Summary

During Week 2, I worked on defining the requirements and workflow for **Rino – AI-Powered Software Engineering Agent**. I explored repository analysis, bug detection, automated testing, GitHub integration, and developer-approved code changes.I spent some time understanding about authentication and authorisation. I also documented the proof of concept, proposed technology stack.

- Finalised the project and understood the objective of the project.
- Defined the boundaries of the project and started researching more on what can be done and what comes under future scope.
- Refined the User workflow and also rewrote the information with more specific details in the Project Info.
- Worked on the first POC after understanding it's importance.
- Created wireframes for Admin and Developer showing the 5 main interfaces to understand how it works.
- Built a small working prototype and played around with it to understand it better.
- Also documented the agent workflow and bug triage rules.
- Worked on GitHub integration, authentication, authorization, and logging requirements.
- Also outlined the proposed technology stack and system components.


## 2. Tasks Completed

- **Project Requirements:** 
    - Defined the project's objectives, problem statement, proposed solution, and core workflow.
- **Agent Workflow:** 
    - Documented the five stages: 
        - Repository connection
        - Test execution 
        - Bug triage 
        - AI-generated explanations 
        - Suggested fixes.
- **Bug Detection:** 
    - Explore and defined severity levels (**Critical, High, Medium, and Low**) and rules for handling duplicate findings, setup failures, low-confidence results, and security issues.
- **Testing and Analysis:** 
    - Identified few built in tools like pytest, pylint, and bandit for testing, code quality checks, and security analysis.
    - Also explored Dev Instances, GitHub Actions and RINO's own sandbox and ubderstood their tradeoffs.
- **GitHub Integration:** 
    - Documented repository access, authentication, Admin and Developer roles, GitHub Issues, commit history, CI logs, and pull requests. Here, we decided to go with GitHub App for auth.
- **Fix Validation:** 
    - Defined the need to retest suggested code changes and get a human approval for security issues and significant modifications.
- **Technology Stack:** 
    - Identified Next.js, TypeScript, FastAPI, Python, PostgreSQL, Redis, and Docker for the proposed architecture.
- **Git and Environment Setup:** 
    - Practiced repository cleanup, .gitignore rules, branch management, pull requests, and code reviews.
- **GitHub activity:**
    - Created a new branch for project with the name "AI_Powered_Software_Agent"
    - Understood more about raising a PR, it's importance, how to merge, how to resolve the conflicts, how it would effect other branches.
    - Renamed and moved Weekly reports, created a seperate folder for each of us and moved our report into that folder.
    - Defined GitHub rules for main branch to have atleast 1 reviewer approve a PR before letting it merge with the main. 

## 3. Key Outcomes

- Established a clearer scope for the first version of Rino.
- Defined how rule-based triage and AI-generated explanations will work together.
- Identified the importance of test evidence, secure repository access, duplicate detection, and audit logs.
- Consolidated the initial functional requirements and technical design decisions in the POC documentation.
