# Local Issue Analyzer Agent

### Problem Statement Definition
Local governments and community organizers are constantly inundated with raw, unstructured feedback, sentiment, and reports regarding community issues like social media complaints, direct messages, public reporting forms. 
This data is characterized by:
- High Volume & Velocity: Too much data is generated too quickly to process manually.

- Lack of Structure: Reports often use inconsistent language, contain noise, and combine multiple issues into a single message.

- Absence of Priority: Without manual triage, it is impossible to quickly discern which issues (e.g., potholes vs. non-functional streetlights) are the most critical, frequent, or impactful to the community.

The core problem is the inefficient and subjective prioritization of public concern, leading to delayed or misallocated resources for necessary community improvements.

### How an Agent Can Help
A multi-agent system, specifically a Sequential Agent built using the Gemini ADK, provides the perfect structure to solve this. An agent-based approach offers several advantages:

- Automation: It autonomously processes vast amounts of unstructured text data, eliminating the need for tedious manual reading and categorization.

- Specialization (The Pipeline): By breaking down the complex task into specialized sub-agents (Harvester, Classifier, Prioritizer), each stage can focus on a single, highly accurate task (data collection, categorization, ranking).

- Contextual Understanding: Large Language Models (LLMs) excel at natural language understanding, allowing the agent to grasp the nuance, emotion, and context of public complaints that simple keyword filters would miss.

- Structured Output: The final agent is instructed to produce a structured, machine-readable report (JSON/Dict), which can be easily consumed by dashboards or resource allocation systems.

### Working of the Agent & Its Logic
The Local Issue Analyser is implemented as a three-stage SequentialAgent pipeline, guaranteeing that data flows logically and reliably from raw text to prioritized insights.  This design ensures that the output of one specialized agent becomes the precise input for the next, moving the data toward its final, structured form. The main main_api.py then executes this pipeline using run_debug and employs robust extraction logic to cleanly separate the machine-consumable JSON report from the final text summary for human review.

The sequential flow involves three distinct sub-agents:

1. Harvester Agent
> Role & Input: This agent receives the initial user prompt (e.g., "Analyze reports about road quality and public safety in Mumbai") and is responsible for data collection.

> Logic and Output: It utilizes an external tool (such as Google Search or a custom search_local_news tool) to find and consolidate relevant raw public reports, articles, and sentiment data. The output is a single, large chunk of consolidated, raw text data.

2. Classifier Agent
> Role & Input: This agent receives the raw, consolidated text data directly from the Harvester Agent. It performs data structuring and categorization.

> Logic and Output: It meticulously processes the unstructured text to identify unique, discrete issues (like "Potholes on Main Street" or "Increase in petty theft"). It then categorizes these issues into higher-level groups (e.g., Infrastructure, Safety, Services). The output is a list or table of categorized, unique issues, presented in a clean text or markdown format.

3. Prioritizer Agent
> Role & Input: This agent receives the categorized list of unique issues from the Classifier Agent and acts as the final decision-maker.

> Logic and Output: It analyzes the frequency, severity, and urgency implied in the reports for each unique issue. It then assigns a quantitative priority score (e.g., 1-10) to each item. Crucially, it converts its final findings into a highly reliable JSON format, which serves as the final, ranked structured report. The final output visible to the user is the human-readable summary of this JSON report, provided by the Sequential Agent itself.

### Conclusion
The Local Issue Analyser represents a modern, robust application of the Gemini ADK for civic technology. By combining specialized agents within a sequential pipeline, it transforms chaotic public feedback into actionable, objective, and prioritized intelligence. This efficient shift from manual triage to automated, structured reporting empowers local authorities to improve resource management and respond more effectively to the most pressing needs of their communities.