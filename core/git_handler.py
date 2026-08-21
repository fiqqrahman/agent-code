from pathlib import Path
import git


class GitHandler:
    SUPPORTED_EXTENSIONS = {".php", ".py", ".js", ".ts", ".go", ".java", ".c", ".cpp"}

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

        for ignored in self.IGNORED_PATHS:
            if normalized_path.startswith(ignored) or f"/{ignored}" in normalized_path:
                return False

        return Path(file_path).suffix in self.SUPPORTED_EXTENSIONS

    def _safe_decode_patch(self, diff_content: bytes | str | None) -> str:
        if isinstance(diff_content, bytes):
            return diff_content.decode("utf-8", errors="replace")
        elif isinstance(diff_content, str):
            return diff_content
        return ""

    def get_working_tree_diff(self) -> list[dict[str, str]]:
        diff_files: list[dict[str, str]] = []
        seen_paths: set[str] = set()

        # 1. Cek file yang dimodifikasi (Unstaged Modified)
        for diff_item in self.repo.index.diff(None):
            file_path = diff_item.b_path or diff_item.a_path
            if file_path and self._is_valid_target_file(file_path):
                patch_text = self._safe_decode_patch(diff_item.diff)
                if patch_text.strip():
                    diff_files.append(
                        {"file_path": str(file_path), "patch": patch_text}
                    )
                    seen_paths.add(str(file_path))

        # 2. Cek file baru yang belum di-track (Untracked)
        for untracked in self.repo.untracked_files:
            if self._is_valid_target_file(untracked) and untracked not in seen_paths:
                full_path = self.repo_path / untracked
                try:
                    content = full_path.read_text(encoding="utf-8", errors="replace")
                    if content.strip():
                        diff_files.append(
                            {"file_path": str(untracked), "patch": content}
                        )
                        seen_paths.add(str(untracked))
                except Exception:
                    pass

        return diff_files

    def get_last_commit_diff(self) -> list[dict[str, str]]:
        diff_files: list[dict[str, str]] = []
        try:
            commit_head = self.repo.head.commit
            if commit_head.parents:
                parent = commit_head.parents[0]
                diffs = parent.diff(commit_head, create_patch=True)
            else:
                diffs = commit_head.diff(git.NULL_TREE, create_patch=True)

            for diff_item in diffs:
                file_path = diff_item.b_path or diff_item.a_path
                if self._is_valid_target_file(file_path):
                    patch_text = self._safe_decode_patch(diff_item.diff)
                    if patch_text.strip():
                        diff_files.append(
                            {"file_path": str(file_path), "patch": patch_text}
                        )
        except Exception:
            pass

        return diff_files
