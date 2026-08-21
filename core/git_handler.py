from pathlib import Path
import git


class GitHandler:
    SUPPORTED_EXTENSIONS = {".php", ".py", ".js", ".ts", ".go", ".java", ".c", ".cpp"}

    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path).resolve()
        if not (self.repo_path / ".git").exists():
            raise ValueError(f"Path bukan repositori Git valid: {self.repo_path}")
        self.repo = git.Repo(self.repo_path)

    def _safe_decode_patch(self, diff_content: bytes | str | None) -> str:
        if isinstance(diff_content, bytes):
            return diff_content.decode("utf-8", errors="replace")
        elif isinstance(diff_content, str):
            return diff_content
        return ""

    def get_working_tree_diff(self) -> list[dict[str, str]]:
        diff_files: list[dict[str, str]] = []
        diffs = self.repo.index.diff(None)

        for diff_item in diffs:
            file_path = diff_item.b_path or diff_item.a_path
            if file_path and Path(file_path).suffix in self.SUPPORTED_EXTENSIONS:
                patch_text = self._safe_decode_patch(diff_item.diff)
                diff_files.append({"file_path": file_path, "patch": patch_text})

        return diff_files

    def get_commit_diff(
        self, commit_a: str, commit_b: str = "HEAD"
    ) -> list[dict[str, str]]:
        diff_files: list[dict[str, str]] = []
        target_a = self.repo.commit(commit_a)
        target_b = self.repo.commit(commit_b)

        diffs = target_a.diff(target_b, create_patch=True)

        for diff_item in diffs:
            file_path = diff_item.b_path or diff_item.a_path
            if file_path and Path(file_path).suffix in self.SUPPORTED_EXTENSIONS:
                patch_text = self._safe_decode_patch(diff_item.diff)
                diff_files.append({"file_path": file_path, "patch": patch_text})

        return diff_files

    def get_initial_commit_diff(self) -> list[dict[str, str]]:
        diff_files: list[dict[str, str]] = []
        commit = self.repo.head.commit
        diffs = commit.diff(git.NULL_TREE, create_patch=True)

        for diff_item in diffs:
            file_path = diff_item.b_path or diff_item.a_path
            if file_path and Path(file_path).suffix in self.SUPPORTED_EXTENSIONS:
                patch_text = self._safe_decode_patch(diff_item.diff)
                diff_files.append({"file_path": file_path, "patch": patch_text})

        return diff_files
