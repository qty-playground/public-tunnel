# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a documentation and analysis project for "public-tunnel" - a network tunneling solution designed for AI assistants to control devices in non-directly accessible network environments. The project uses structured analysis methodologies to transform requirements into object-oriented designs.

## Project Structure

- `docs/` - Core project documentation
  - `01_requirement.md` - Detailed functional requirements for the public-tunnel system
  - `02_user_story.md` - User stories with acceptance criteria and API test mappings
- `prompts/` - Analysis methodology templates
  - `01_structured_analysis.md` - Iterative concept extraction methodology
  - `02_structured_to_ooa.md` - Structured analysis to OOA class diagram conversion

## Key Concepts

### System Architecture
- **AI Assistant**: External system that submits commands via HTTP API
- **Client**: Target devices that poll for commands and execute them
- **Server**: Passive intermediary that manages command queuing and result storage
- **Session-based**: All operations scoped within sessions for isolation

### Core Features
- HTTP polling-based communication (not WebSocket)
- Sync/async command execution modes with auto-switching
- File upload/download within session scope
- FIFO command queuing per client
- Multi-client collaboration within sessions

## Analysis Methodology

The project follows a structured approach:

1. **Iterative Concept Extraction** - Break down requirements into noun-verb relationships using tree structures
2. **Object-Oriented Analysis** - Transform conceptual trees into UML class diagrams
3. **User Story Mapping** - Convert functional requirements into testable acceptance criteria

## Working with Documentation

- All documents are in Traditional Chinese
- Requirements follow a hierarchical structure: Overview → Core Problems → Solution → System Roles
- User stories include acceptance criteria mapped to specific API endpoints
- Analysis prompts provide step-by-step methodologies for requirements analysis

## Development Context

This appears to be a planning/analysis phase project rather than an implementation. No source code, build systems, or testing frameworks are present. The focus is on thorough requirements analysis and design methodology documentation.