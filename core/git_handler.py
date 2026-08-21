from pathlib import Path
import git


class GitHandler:
    SUPPORTED_EXTENSIONS = {".php", ".py", ".js", ".ts", ".go", ".java", ".c", ".cpp"}

    # Path/Folder bawaan framework/vendor yang wajib diabaikan
    IGNORED_PATHS = {
        "vendor/",
        "system/",
        "node_modules/",
        "public/",
        "writable/",
        "storage/",
        ".git/",
    }

    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path).resolve()
        if not (self.repo_path / ".git").exists():
            raise ValueError(f"Path bukan repositori Git valid: {self.repo_path}")
        self.repo = git.Repo(self.repo_path)

    def _is_valid_target_file(self, file_path: str | None) -> bool:
        if not file_path:
            return False

        normalized_path = file_path.replace("\\", "/")

        # Blacklist folder core / vendor
        for ignored in self.IGNORED_PATHS:
            if normalized_path.startswith(ignored) or f"/{ignored}" in normalized_path:
                return False

        # Whitelist ekstensi
        return Path(file_path).suffix in self.SUPPORTED_EXTENSIONS

    def _safe_decode_patch(self, diff_content: bytes | str | None) -> str:
        if isinstance(diff_content, bytes):
            return diff_content.decode("utf-8", errors="replace")
        elif isinstance(diff_content, str):
            return diff_content
        return ""

    def get_working_tree_diff(self) -> list[dict[str, str]]:
        diff_files: list[dict[str, str]] = []
        diffs = self.repo.index.diff(None)  # Unstaged changes

        for diff_item in diffs:
            file_path = diff_item.b_path or diff_item.a_path
            if self._is_valid_target_file(file_path):
                patch_text = self._safe_decode_patch(diff_item.diff)
                if patch_text.strip():
                    diff_files.append(
                        {"file_path": str(file_path), "patch": patch_text}
                    )

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
            if self._is_valid_target_file(file_path):
                patch_text = self._safe_decode_patch(diff_item.diff)
                if patch_text.strip():
                    diff_files.append(
                        {"file_path": str(file_path), "patch": patch_text}
                    )

        return diff_files

    def get_initial_commit_diff(self) -> list[dict[str, str]]:
        diff_files: list[dict[str, str]] = []
        commit = self.repo.head.commit
        diffs = commit.diff(git.NULL_TREE, create_patch=True)

        for diff_item in diffs:
            file_path = diff_item.b_path or diff_item.a_path
            if self._is_valid_target_file(file_path):
                patch_text = self._safe_decode_patch(diff_item.diff)
                if patch_text.strip():
                    diff_files.append(
                        {"file_path": str(file_path), "patch": patch_text}
                    )

        return diff_files
