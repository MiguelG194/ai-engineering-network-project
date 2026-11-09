# Evaluation Method

The network troubleshooting agent is primarily meant to be used by help-desk users.

The agent is good if it is able to accurately evaluate the network state and provide suggestions for any problems that it may encounter. However, just getting the right answer isn't enough; it should be able to do so efficiently without wasting time by using more tools than necessary.

## Metrics

I came up with three metrics to evaluate my agent on:
* **Tool Usage**: Did the model use the right tools efficiently?
    * 0 - Failure: Used incorrect tools, failed to gather necessary information, or made unnecessary tool calls.
    * 1 - Partial Success: Used mostly appropriate tools but missed something or made unnecessary calls.
    * 2 - Success: Used the appropriate tools efficiently and gathered the necessary information.
* **Justification**: Did the model properly explain its reasoning for its answer?
    * 0 - Failure: Provided no meaningful explanation or made unsupported claims.
    * 1 - Partial Success: Provided some explanation but failed to connect its observations to its conclusion.
    * 2 - Success: Clearly explained its findings and supported its conclusions with information gathered from tools.
* **Final Answer**: Did the model produce an accurate answer with the information that it gathered?
    * 0 - Failure: Produced an inaccurate answer, either by not properly interpretting its gathered information or by making it up.
    * 1 - Partial Success: Produced an answer that identified the problem but provided an incomplete solution.
    * 2 - Success: Produced an answer that properly addresses the problem and uses information that it gathered accurately.

Using these metrics will help evalute how well the agent is at diagnosing network configurations. For example, an agent might perform well on getting the right answer and explaining, but it could do poorly on tool usage. We want the agent to work, but it is not very useful if it wastes time.

## Scoring

When scoring the model, I will use the rubic defined above, giving each metric a score from 0-2. I chose to manually review the test results because I feel like some answers could be correct even if they are worded differently. I also want to evaluate the agent myself rather than rely on another AI model to judge its performance.

## Evaluation Set

The evaluation set contains 24 examples, consisting of 10 bridge-related prompts and 14 host-related prompts. The examples were manually created based on common network troubleshooting tasks that a help-desk user might perform. Bridge prompts focus on interface inspection, bridge membership, STP, VLAN filtering, and overall bridge configuration. Host prompts cover interface states, IPv4 addressing, routing, neighbor tables, packet statistics, and connectivity testing.

The set includes both straightforward questions and harder cases that require interpreting multiple observations. For example, determining whether a bridge is functioning correctly requires examining several configuration details, while diagnosing connectivity requires understanding routing, interface states, and communication between hosts. Some prompts also require actively testing connectivity rather than simply retrieving configuration information. Overall, the examples are designed to evaluate the agent's ability to select appropriate tools, interpret network information, and provide accurate, well-supported troubleshooting explanations.

# Model Selection

## Results

| Agent | Average Response Time | Tool Usage Avg (0-2) | Justification Avg (0-2) | Final Answer Avg (0-2) |
|---|---|---|---|---|
| **llama_local** | 292.76s (~4.88 min) | 1.42 | 0.96 | 1.25 |
| **qwen_local** | 309.87s (~5.16 min) | 1.71 | 0.67 | 1.54 |
| **gemini_cloud** | 375.32s (~6.26 min) | 2 | 2 | 2 |

## Model Justification

The model I decided to continue using was qwen2.5-coder:3b. It demonstrated a stronger understanding of raw system data compared to llama3.2:3b. While Gemini 3.8 Flash provided deeper reasoning and outperformed the other two models in the metrics, it was only able to complete 3 of the 24 tests due to rate limiting. Qwen’s main weakness was presentation rather than comprehension. Moving forward, I plan to further simplify the tools, clean up tool output formats, train Qwen to produce structured responses, and optimize its tool-calling efficiency to reduce execution times.

# Iteration Log

## Table

| Date | What Changed | Score | What I Learned |
|---|---|---|---|
| Nov. 8 | Baseline test (no changes) | 1.51/2.00 | Qwen and Llama understood the available tools reasonably well but struggled with presenting accurate and clear answers. Qwen sometimes confused IP addresses belonging to other hosts with locally assigned addresses, while Llama sometimes selected tools that inspected the wrong VM or misinterpreted Linux networking states. Gemini performed perfectly across all three metrics but had the longest average response time. This showed that correct tool usage does not necessarily guarantee accurate final answers. |

## Failures

| # | Model | Prompt | What Went Wrong | Fix |
|---|---|---|---|---|
| 1 | qwen_local | What IPv4 addresses are assigned to Host A? | The agent incorrectly reported Host B’s IP (192.168.10.2) as belonging to Host A and missed Host A’s actual addresses. It confused neighboring devices’ IPs with addresses assigned locally. | Update the system prompt to instruct the model to use ip addr show to identify local IP addresses instead of relying on ARP tables, neighbor tables, or ping logs. |
| 2 | llama_local | Which network interfaces on Host A are currently operational? | When host_a_get_interfaces() failed to return operational states, the agent incorrectly substituted get_interfaces(), which inspects the Bridge VM. It then reported the bridge's interfaces (br0, enp0s9, enp0s10) as belonging to Host A. | Update host_a_get_interfaces() to return operational link states directly in its JSON response. Also, use clearer tool names to reduce confusion between Host A and Bridge VM tools. |
| 3 | llama_local | Does the current bridge configuration appear to be functioning correctly? | The model produced a false negative diagnosis, claiming the bridge was failing because the loopback (lo) interface reported an UNKNOWN state and STP/VLAN filtering were turned off. | Investigate using RAG to help the model understand Linux networking terminology. Alternatively, add a brief explanation of these concepts to the system prompt. |
