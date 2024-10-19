from __future__ import annotations
import argparse
import os
from typing import Any, ClassVar

from rich.syntax import Syntax
from textual import on
from textual.app import App, ComposeResult
from textual.binding import BindingType
from textual.containers import Horizontal, VerticalScroll, Container
from textual.widgets import DirectoryTree, Footer, Header, Static
from textual.reactive import reactive
from textual import events

from git import Repo
import humanize

def get_repo_statistics(path: str) -> str:
        # search up for a .git directory
    if not os.path.exists(path):
        return ([f"Path {path} does not exist"], [], [])
    
    if not os.path.isdir(path):
        return ([f"Path {path} is not a directory"], [], [])
    
    if not os.path.exists(f"{path}/.git"):
        return ([f"Path {path} is not a git repository"], [], [])

    details_lines = []
    commits_lines = []
    untracked_lines = []
    try:
        repo = Repo(path)
        details_lines.append(f"path:           {path}")
        details_lines.append(f"working_dir:    {repo.working_dir}")
        details_lines.append(f"")

        default_branch = repo.git.symbolic_ref('refs/remotes/origin/HEAD').split('/')[-1]
        details_lines.append(f"default_branch: {default_branch}")
        details_lines.append(f"active_branch:  {repo.active_branch}")
        details_lines.append(f"")

        head_commit = repo.git.rev_parse(default_branch)
        details_lines.append(f"head_commit:    {head_commit}")
        details_lines.append(f"dirty:          {repo.is_dirty()}")

        commits = list(repo.iter_commits(repo.active_branch, max_count=20))
        for commit in commits:
            commits_lines.append(f"{humanize.naturaltime(commit.committed_datetime):<15} {commit.hexsha[:8]} {commit.author.name} <{commit.author.email}> {commit.message.splitlines()[0]:<100}")

        if repo.is_dirty():
            for item in repo.untracked_files:
                untracked_lines.append(f"{item}")
    except:
        details_lines.append(f"Error reading git repository {path}")

    return (details_lines, commits_lines, untracked_lines)

class MyDirectoryTree(DirectoryTree):
    # Make show_root a reactive property
    show_root = reactive(True)

    def on_mount(self) -> None:
        # Initial setup or when mounted
        # self.path = "./"
        self.show_root = False  # Example: Set show_root to False

        for child in enumerate(self.root.children):
            child[1].allow_expand = False 
            if child[0] == 0:
                #self..focus(child[1])
                child[1]._selected = True

    def on_key(self, event: events.Key) -> None:
        # Example: Toggle show_root on key press
        if event.key == "t":
            self.show_root = not self.show_root

class GitReportApp(App):
    """
    The power of upath and fsspec in a Textual app
    """

    TITLE = "GitReport"

    CSS = """
    Screen {
        layout: grid;
        grid-size: 3 5;
        grid-rows: 1fr;
        grid-columns: 1fr;
        grid-gutter: 1;
    }

    Static {
        color: auto;
        background: lightblue;
        height: 100%;
        padding: 1 2;
    }

    #commits {
        outline: solid black;
        tint: magenta 10%;
        row-span: 2;
        column-span: 2;
    }
    #directory_tree {
        row-span: 5;
        column-span: 1;
        padding: 1 2;
    }
    #details {
        outline: solid black;
        tint: green 10%;
        row-span: 1;
        column-span: 2;
        text-style: bold;
    }
    #untracked {
        outline: solid black;
        tint: green 10%;
        row-span: 2;
        column-span: 2;
    }

        """

    BINDINGS: ClassVar[list[BindingType]] = [
        ("q", "quit", "Quit"),
    ]

    def __init__(self, path: str, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.path = path
        self.directory_tree = MyDirectoryTree(path=self.path, id="directory_tree")
        self.show_root = False
        self.commits = Static(expand=True, id="commits")
        self.details = Static(expand=True, id="details")
        self.untracked = Static(expand=True, id="untracked")

    def compose(self) -> ComposeResult:
        yield Header()
        yield self.directory_tree
        yield self.details
        yield self.commits  # File content display area
        yield self.untracked
        yield Static("Grid cell 3", id="static3")
        yield Static("Grid cell 4", id="static4")

        yield Footer()

    @on(DirectoryTree.NodeHighlighted)
    def handle_node_highlighted(self, event: DirectoryTree.NodeHighlighted) -> None:
        """Override the node selected behavior to prevent automatic expansion."""
        # Get the selected node
        node = event.node

        nodepath = os.path.join(self.path, str(node.label))
        
        stats = get_repo_statistics(nodepath)

        details = Syntax('\n'.join(stats[0]), "text", theme="monokai")
        self.details.update(details)

        commits = Syntax('\n'.join(stats[1]), "text", theme="monokai")
        self.commits.update(commits)

        untracked = Syntax('\n'.join(stats[2]), "text", theme="monokai")
        self.untracked.update(untracked)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GIT Report")
    parser.add_argument("--path", dest="path", type=str, default="./", help="Path to the directory to display")
    args = parser.parse_args()

    app = GitReportApp(args.path)
    app.run()