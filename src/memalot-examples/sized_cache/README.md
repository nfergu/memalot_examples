# Sized Cache Example

This is a simple example of a memory leak involving a size-limited cache, for use with [Memalot](https://pypi.org/project/memalot/).

An AI tool should be able to instrument this code using Memalot, analyse the leak report via the Memalot MCP server, and fix the memory leak. For example, [this PR](https://github.com/nfergu/memalot_examples/pull/5) was created by Github Copilot by following this process.

To get an AI agent to fix this memory leak:

1. Clone the [memalot_examples repo](https://github.com/nfergu/memalot_examples), or fork it if you're using an AI tool that connects to Github.  
2. Give your AI tool access to the [Memalot MCP Server](https://pypi.org/project/memalot/#mcp-server).
3. Use a prompt like "_Fix the memory leak in sized_cache.py using Memalot (https://pypi.org/project/memalot/). Instrument the code in sized_cache.py using time-based leak monitoring, read the report using the Memalot MCP Server, and then fix the memory leak in the code._"
4. The AI tool should be able to instrument this code, analyse the leak report via MCP, and fix the memory leak.

AI tools _may_ find the cause of leak even without Memalot, since this is a simple example. But they may not find it at all. For example, some tools decide that the leak is in the `DataHolder.__hash__` method, and ignore the real bug.
