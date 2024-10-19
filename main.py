from __future__ import annotations
import argparse
import os
from typing import Any, ClassVar

from rich.syntax import Syntax
from textual import on
from textual.app import App, ComposeResult
from textual.binding import BindingType
from textual.containers import Horizontal, VerticalScroll
from textual.widgets import DirectoryTree, Footer, Header, Static
from textual.reactive import reactive
from textual import events

from git import Repo

def get_git_stats(path: str) -> str:
        # search up for a .git directory
    if not os.path.exists(path):
        return (f"Path {path} does not exist")
    
    if not os.path.isdir(path):
        return (f"Path {path} is not a directory")
    
    if not os.path.exists(f"{path}/.git"):
        return (f"Path {path} is not a git repository")

    contents = [f"path: {path}"]
    try:
        repo = Repo(path)
        contents.append(f"working_dir: {repo.working_dir}")
        default_branch = repo.git.symbolic_ref('refs/remotes/origin/HEAD').split('/')[-1]
        contents.append(f"default_branch: {default_branch}")
        contents.append(f"active_branch: {repo.active_branch}")
        head_commit = repo.git.rev_parse(default_branch)
        contents.append(f"head_commit: {head_commit}")
        contents.append(f"Dirty: {repo.is_dirty()}")

        contents.append("Last 5 commits:")
        commits = list(repo.iter_commits(repo.active_branch, max_count=5))
        for commit in commits:
            contents.append(f"Commit: {commit.hexsha}")
            contents.append(f"Author: {commit.author.name} <{commit.author.email}>")
            contents.append(f"Date: {commit.committed_datetime}")
            contents.append(f"Message: {commit.message}")

        if repo.is_dirty():
            for item in repo.untracked_files:
                contents.append(f"Untracked file: {item}")
    except:
        contents.append("Error reading git repository")

    return Syntax(
        '\n'.join(contents),
        "text",
        theme="monokai",
    )

class MyDirectoryTree(DirectoryTree):
    # Make show_root a reactive property
    show_root = reactive(True)

    def on_mount(self) -> None:
        # Initial setup or when mounted
        # self.path = "./"
        self.show_root = False  # Example: Set show_root to False

    def on_key(self, event: events.Key) -> None:
        # Example: Toggle show_root on key press
        if event.key == "t":
            self.show_root = not self.show_root

class DirectoryTreeApp(App):
    """
    The power of upath and fsspec in a Textual app
    """

    TITLE = "DirectoryTree"

    CSS = """
    DirectoryTree {
        max-width: 50%;
        width: auto;
        height: 100%;
        dock: left;
    }
    """

    BINDINGS: ClassVar[list[BindingType]] = [
        ("q", "quit", "Quit"),
    ]

    def __init__(self, path: str, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.path = path
        self.directory_tree = MyDirectoryTree(path=self.path)
        self.show_root = False
        self.file_content = Static(expand=True)

    def compose(self) -> ComposeResult:
        yield Header()
        yield Horizontal(self.directory_tree, VerticalScroll(self.file_content))
        yield Footer()

    @on(DirectoryTree.NodeHighlighted)
    def handle_node_highlighted(self, event: DirectoryTree.NodeHighlighted) -> None:
        """Override the node selected behavior to prevent automatic expansion."""
        # Get the selected node
        node = event.node
        node.allow_expand = False

        nodepath = os.path.join(self.path, str(node.label))
        
        stats = get_git_stats(nodepath)
        self.file_content.update(stats)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GIT Report")
    parser.add_argument("--path", dest="path", type=str, default="./", help="Path to the directory to display")
    args = parser.parse_args()

    app = DirectoryTreeApp(args.path)
    app.run()