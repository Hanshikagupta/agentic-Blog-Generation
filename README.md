# Blog Writing Agent

An AI-powered blog writing agent that automatically generates technical blog posts from a given topic. The agent handles research, planning, content generation, and image creation.

## Features

- **Smart Routing**: Automatically decides if web research is needed (closed-book, hybrid, or open-book modes)
- **Web Research**: Integrates with Tavily Search API for up-to-date information
- **Content Planning**: Creates a structured outline with multiple tasks
- **Parallel Writing**: Generates multiple blog sections in parallel
- **Image Generation**: Automatically plans and generates images using Gemini
- **Terminal-Based Input**: Get blog topics directly from terminal input

## Requirements

### Dependencies

```bash
pip install -r requirements.txt
```

Key packages:
- `langgraph` - Graph orchestration
- `langchain-openai` - OpenAI LLM integration
- `langchain-community` - Community tools (Tavily search)
- `google-genai` - Gemini image generation
- `pydantic` - Data validation
- `python-dotenv` - Environment variable management

### Environment Variables

Create a `.env` file in the project directory with:

```env
OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
```

**Note**: 
- `OPENAI_API_KEY` is required
- `TAVILY_API_KEY` is required only if you want web research
- `GOOGLE_API_KEY` is required only if you want image generation

## Usage

### Basic Usage

Run the script from the terminal:

```bash
python bog.py
```

The script will prompt you for:
1. **Blog topic** - The main subject of the blog post
2. **As-of date** - Publication date (optional, defaults to today)

Example:
```
============================================================
Blog Writing Agent
============================================================

Enter blog topic: How to use LangGraph for AI workflows
Enter as-of date (YYYY-MM-DD) [default: today]: 
```

### Output

The script generates:
1. **Console Output**: Full blog content displayed in the terminal
2. **Markdown File**: Saved with the blog title (e.g., `how_to_use_langgraph_for_ai_workflows.md`)
3. **Images Directory**: Optional `images/` folder with generated diagrams
4. **Plan Summary**: Overview of the blog structure with tasks

## Architecture

### Graph Flow

```
START
  ↓
ROUTER (Decide if research needed)
  ↓
[RESEARCH] (Optional - fetch web data)
  ↓
ORCHESTRATOR (Create blog plan)
  ↓
WORKER (Generate sections in parallel)
  ↓
REDUCER (Merge, plan images, generate images)
  ↓
END
```

### Key Components

1. **Router Node**: Determines routing strategy (closed_book/hybrid/open_book)
2. **Research Node**: Performs web searches via Tavily
3. **Orchestrator Node**: Creates detailed blog outline
4. **Worker Node**: Writes individual blog sections
5. **Reducer Subgraph**:
   - Merge content sections
   - Decide which images are needed
   - Generate images via Gemini

## Modes

- **closed_book**: No research needed (evergreen concepts)
- **hybrid**: Blend of evergreen content with recent examples
- **open_book**: News/event-driven content (requires research)

## Blog Kinds

Supported blog types:
- `explainer` - Conceptual explanations
- `tutorial` - Step-by-step guides
- `news_roundup` - Weekly/topical roundup
- `comparison` - Comparison between technologies
- `system_design` - Architecture deep-dives

## File Structure

```
blog/
├── bog.py              # Main agent script
├── README.md           # This file
├── .env                # Environment variables (create this)
├── *.md                # Generated blog posts
└── images/             # Generated blog images
```

## Example Output

```markdown
# How to Use LangGraph for AI Workflows

## Introduction
[Content about LangGraph...]

## Getting Started
[Installation and setup...]

## Building Your First Graph
[Example code and explanation...]

## Advanced Patterns
[More complex workflows...]
```

## Troubleshooting

### No API Key Error
```
Error: OPENAI_API_KEY is not set.
```
Solution: Add your OpenAI API key to the `.env` file

### Research Not Working
```
Error: TAVILY_API_KEY is not set.
```
Solution: The agent will skip research. Add a Tavily API key to `.env` if you need it.

### Image Generation Failed
```
Error: GOOGLE_API_KEY is not set.
```
Solution: The blog will be generated without images. Add a Google API key to `.env` if you need images.

### Empty or Poor Quality Output
- Make sure your topic is specific and detailed
- Check that API keys are valid
- Try a different topic if the API limits are hit

## Performance Notes

- First run may take 2-5 minutes depending on:
  - Research requirements
  - Number of blog sections (typically 5-9)
  - Image generation (if enabled)
- Subsequent runs with same topic may cache results from API calls

## Configuration

### Model Selection

Edit `bog.py` to change the LLM:

```python
llm = ChatOpenAI(model="gpt-4o-mini")  # Change model here
```

Available options:
- `gpt-4o-mini` (default, faster)
- `gpt-4o` (better quality)
- Other OpenAI models

## Contributing

To extend the agent:
1. Add new node functions to `bog.py`
2. Connect them in the graph definition
3. Update this README with new features

## License

MIT License

## Support

For issues or questions, check:
1. `.env` file has all required API keys
2. API keys are valid and have sufficient quota
3. Required packages are installed: `pip install -r requirements.txt`
