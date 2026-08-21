import sys
from dotenv import load_dotenv
from core.auditor import CodeAuditor
from core.git_handler import GitHandler
from utils.formatter import AuditFormatter

load_dotenv()


def main():
    AuditFormatter.print_banner()

    target_repo = sys.argv[1] if len(sys.argv) > 1 else "."

    try:
        auditor = CodeAuditor()
        git_engine = GitHandler(repo_path=target_repo)

        AuditFormatter.print_info(f"Memindai repositori di: {git_engine.repo_path}")

        # 1. Cek Unstaged Changes
        diff_files = git_engine.get_working_tree_diff()

        # 2. Cek Commit biasa jika working tree bersih
        if not diff_files:
            AuditFormatter.print_info(
                "Working tree bersih. Mengambil perubahan dari COMMIT TERAKHIR..."
            )
            try:
                diff_files = git_engine.get_commit_diff("HEAD~1", "HEAD")
            except Exception:
                # 3. Fallback ke Initial Commit
                AuditFormatter.print_info(
                    "Mendeteksi Initial Commit. Mengambil patch commit awal..."
                )
                try:
                    diff_files = git_engine.get_initial_commit_diff()
                except Exception as err:
                    AuditFormatter.print_error(
                        f"Gagal mengambil patch commit awal: {str(err)}"
                    )

        if not diff_files:
            AuditFormatter.print_info(
                "Tidak ada diff commit ditemukan pada repositori ini."
            )
            return

        # 4. Eksekusi Audit
        for item in diff_files:
            AuditFormatter.print_info(f"Mengaudit file: {item['file_path']}")
            report = auditor.audit_source_code(
                source_code=item["patch"], file_name=item["file_path"]
            )
            AuditFormatter.print_section(f"GIT DIFF AUDIT: {item['file_path']}", report)

    except Exception as err:
        AuditFormatter.print_error(f"Eksekusi Audit Gagal: {str(err)}")


if __name__ == "__main__":
    main()
