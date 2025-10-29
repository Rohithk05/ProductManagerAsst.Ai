> AI-powered tool to generate Product Requirements Documents (PRDs) and professional API documentation from code
A comprehensive tool that bridges product strategy and technical documentation. Generate detailed PRDs with user stories, success metrics, and risk analysis—while simultaneously auto-generating professional API documentation (Markdown, OpenAPI specs, code examples) from your codebase.
## Features

### PRD Generator
- 📋 **Professional PRDs**: Auto-generates complete Product Requirements Documents
- 👤 **User stories**: Creates detailed user stories with acceptance criteria
- 📊 **Success metrics**: Defines measurable KPIs and success criteria
- ⏱️ **Timeline estimates**: Provides realistic development timelines
- ⚠️ **Risk analysis**: Identifies risks and mitigation strategies
- 🎨 **Multiple optimization styles**: ATS, Creative, Aggressive modes

### API Documentation Generator
- 📚 **Markdown docs**: Beautiful, professional API documentation
- 🔗 **OpenAPI 3.0 specs**: Valid, production-ready OpenAPI specifications
- 💻 **Code examples**: Working code samples in multiple languages
- 🔧 **Multi-language support**: Python, JavaScript, Go, Java
- 📤 **Export ready**: Copy-paste output for immediate use

## Tech Stack

### Backend
- **FastAPI** - High-performance Python framework
- **Groq API** - Ultra-fast LLM inference (Llama 3.3 70B)
- **Python** - Backend logic and documentation generation

### Frontend
- **HTML5 + Tailwind CSS** - Modern, responsive UI
- **Vanilla JavaScript** - Interactive tabs and forms
- **Marked.js** - Markdown rendering
- **Highlight.js** - Code syntax highlighting

## Installation

### Prerequisites
- Python 3.8+
- Groq API Key (free tier at https://console.groq.com)
### Setup

1. **Clone the repository**
2. **Create virtual environment**
3. **Install dependencies**
4. **Configure API key**
5. **Run the application**
6. **Open in browser**
Navigate to http://localhost:8002

## Usage

### Generate PRD
1. Go to "📋 PRD Generator" tab
2. Enter feature idea
3. Specify target audience
4. Add problem statement (optional)
5. Click "🚀 Generate PRD"
6. View PRD, User Stories, and Success Metrics in separate tabs
7. Copy and share with stakeholders

### Generate API Documentation
1. Go to "📚 API Doc Generator" tab
2. Enter project name
3. Select programming language
4. Paste your API code
5. Click "📚 Generate Docs"
6. View Markdown, OpenAPI spec, and code examples
7. Export and use in your project

## Example Use Cases

### For Product Managers
- 📝 Quickly create detailed PRDs from rough ideas
- 📊 Define success metrics and KPIs upfront
- ⚠️ Identify risks before development starts
- 👥 Communicate clearly with engineering teams

### For Developers & Architects
- 📚 Auto-generate professional API documentation
- 🔗 Create valid OpenAPI specs without manual work
- 💻 Generate code examples in multiple languages
- 🚀 Onboard new developers faster

### For Startups & MVPs
- ⚡ Move fast with AI-generated documentation
- 💰 Reduce documentation overhead
- 📋 Maintain consistency across products
- 🤝 Improve team communication

## API Endpoints

### POST `/api/generate-prd`
Generates a comprehensive Product Requirements Document

**Response**: PRD document, user stories, metrics, timeline, risks

### POST `/api/generate-api-docs`
Generates API documentation from code

**Response**: Markdown docs, OpenAPI spec, code examples

## Performance

- ⚡ **PRD generation**: 3-8 seconds
- 📚 **API docs generation**: 2-5 seconds
- 💰 **Cost**: Free (uses Groq's free tier)
- 🔄 **Concurrent requests**: Handles multiple requests

## Output Quality

- ✅ **Professional standards**: Follows industry best practices
- ✅ **Valid specs**: OpenAPI 3.0.0 compliant
- ✅ **Actionable insights**: Specific, measurable, achievable goals
- ✅ **Comprehensive**: Includes all sections needed for stakeholder communication

## Browser Support

- Chrome/Chromium ✅
- Firefox ✅
- Safari ✅
- Edge ✅

## Roadmap

- [ ] GitHub integration for automated documentation
- [ ] Confluence/Notion export
- [ ] Team collaboration and version control
- [ ] Template library for PRDs
- [ ] Real-time collaboration
- [ ] Slack/Teams integration
- [ ] Multi-language PRD generation
- [ ] Custom branding for documents

## Contributing

Contributions are welcome! Feel free to submit issues and pull requests.

## License

MIT License - see LICENSE file for details

## Author

Built with ❤️ using Groq + Llama 3.3 70B

---

**If this tool saves you time, please consider starring it!** ⭐

## Support

For issues, questions, or feedback, please open an issue on GitHub.



