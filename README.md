# An agent that uses Dropbox tools provided to perform any task

## Purpose

# Introduction
Welcome to the Dropbox AI Agent! This agent is designed to assist you in managing your files on Dropbox efficiently. Whether you need to search for specific documents, list items in a folder, or download necessary files, the agent can streamline these tasks for you. By utilizing various tools, it can interact with your Dropbox storage seamlessly.

# Instructions
1. **Search for Files or Folders**: Use the search tool to find specific items based on keywords. 
2. **List Items in a Folder**: Browse the contents of a specific folder to see what files and folders are available.
3. **Download Files**: Download any file found using the previous workflows by providing either the file path or file ID.

# Workflows
## Workflow 1: Search for Files or Folders  
- **Tool**: `Dropbox_SearchFilesAndFolders`  
- **Parameters**: 
  - `keywords`: The terms you want to search for in your Dropbox.
  - `search_in_folder_path`: Optional folder path for more specific searches.
  - `limit`: Maximum number of items to return (default is 100). 
  
## Workflow 2: List Items in a Folder  
- **Tool**: `Dropbox_ListItemsInFolder`  
- **Parameters**: 
  - `folder_path`: Path to the folder you want to browse.
  - `limit`: Maximum number of items to return (default is 100).  

## Workflow 3: Download a File  
- **Tool**: `Dropbox_DownloadFile`  
- **Parameters**: 
  - `file_path` or `file_id`: Provide the path or ID of the file you wish to download.  

By following these workflows, the agent can efficiently handle your Dropbox tasks, making file management easier and quicker.

## MCP Servers

The agent uses tools from these Arcade MCP Servers:

- Dropbox

## Getting Started

1. Install dependencies:
    ```bash
    bun install
    ```

2. Set your environment variables:

    Copy the `.env.example` file to create a new `.env` file, and fill in the environment variables.
    ```bash
    cp .env.example .env
    ```

3. Run the agent:
    ```bash
    bun run main.ts
    ```