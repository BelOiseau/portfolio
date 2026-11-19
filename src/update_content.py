import requests
import os
import shutil
import json
import mdformat
from dotenv import load_dotenv
from typing import Any
from text_conversion import extract_title, format_md


def import_notion_pages_to_folder(folder: str) -> str:
    load_dotenv()
    api_key = os.environ.get("NOTION_API_TOKEN")
    notion_version = os.environ.get("NOTION_VERSION")

    try:
        print(f"Searching notion pages...")
        response = search_notion_pages(api_key, notion_version)
    except Exception as e:
        return f"ERROR: {e}"
    if response.get("object") == "error":
        return format_error(response, "Searching notion pages failed")
    results = response.get("results")

    shutil.rmtree(folder, ignore_errors=True)
    print(f"Creating '{folder}' folder")
    os.mkdir(folder)

    for page in results:
        try:
            response = get_page_markdown(page, api_key, notion_version)
        except Exception as e:
            return f"ERROR: {e}"
        if response.get("object") == "error":
            print(format_error(response, "getting markdown page failed"))
            continue

        unformatted_md = response.get("markdown") + "\n"
        preformatted_md = format_md(unformatted_md)
        formatted_md = mdformat.text(preformatted_md, options={"number": True})
        page_path = page.get("properties").get("URL").get("url")
        load_content(folder, formatted_md, page_path)

    return f"SUCCES: all pages were imported successfully in '{folder}'"
    
def format_error(error: dict[str, str], name: str) -> str:
    formated_error = []
    formated_error.append(f"ERROR: {name}")
    for key, value in error.items():
        formated_error.append(f"{key}: {value}")
    return "\n".join(formated_error)

def load_content(dir_path_content: str, markdown: str, page_path: str) -> None:
    endpoint = os.path.join(dir_path_content, page_path)
    if not os.path.exists(endpoint):
        print(f"Creating {endpoint}")
        os.makedirs(endpoint, exist_ok=True)

    try:
        title = extract_title(markdown)
    except:
        title = "unknown title"
    print(f"Loading '{title}' in {endpoint}")
    html_file = os.path.join(endpoint, "index.md")
    with open(html_file, "w") as f:
        f.write(markdown)
        
def search_notion_pages(api_key: str, notion_version: str) -> list[dict[str, str]]:
    url = "https://api.notion.com/v1/search"
    payload = {
        "filter": {
            "property": "object",
            "value": "page",
            "in_trash": False
        }
    }
    headers = {
        "Notion-Version": notion_version,
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers).json()
    return response

def get_page_markdown(
        page: dict[str, Any], api_key: str, notion_version: str
    ) -> dict[str, Any]:
    page_id = page.get("id")

    url = f"https://api.notion.com/v1/pages/{page_id}/markdown"
    headers = {
        "Notion-Version": notion_version,
        "Authorization": f"Bearer {api_key}"
    }
    response = requests.get(url, headers=headers).json()
    return response

if __name__ == "__main__":
    print(import_notion_pages_to_folder("content"))