# Sample Q&A — Agent Testing

Tested against the deployed agent in the Azure AI Foundry Playground.

> Where the knowledge source doesn't contain an answer, the agent correctly
> says so instead of hallucinating — see Q3 below.

---

**Greeting**

> Hii

Agent response:
> Hi! I'm the Smartbridge Salesforce AI Assistant. I can help with questions
> about Salesforce's AI capabilities (Einstein, Agentforce, Copilot, Prompt
> Builder, Data Cloud AI, etc.) — what would you like to know?

---

**Q1: What is the main objective of Salesforce Einstein Copilot?**

Agent response:
> The main objective of Einstein Copilot is to turn your Salesforce and
> enterprise data into conversational, actionable insights and automations —
> so users can ask questions (e.g., about an account, opportunity, or order)
> and get meaningful, context-aware answers, summaries, recommendations, and
> actions directly inside Salesforce.
>
> Would you like an example use case (sales, service, or marketing) showing
> how Copilot delivers those insights?

---

**Q2: What AI companies did Salesforce acquire?**

Agent response:
> I don't have the names of Salesforce's AI-company acquisitions in my
> current knowledge source. The material I have only says Salesforce
> acquired three AI/data-science companies between 2014 and 2017 but does
> not list them.
>
> I can either:
> - Help with questions about Salesforce's AI features (Einstein Copilot,
>   Data Cloud, Prompt Builder, etc.) using this source, or
> - Look up the specific acquisition names for you if you'd like me to
>   search the web. Which would you prefer?

*This response is a good demonstration of grounded behavior — the agent
declines to guess at facts not present in the transcript and instead offers
a clear, honest fallback, rather than hallucinating company names.*

---

