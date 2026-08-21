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

        AuditFormatter.print_info(f"Target Repositori: {git_engine.repo_path}")

        diff_files = git_engine.get_working_tree_diff()

        if not diff_files:
            AuditFormatter.print_info(
                "Working tree bersih. Memeriksa file pada COMMIT TERAKHIR..."
            )
            diff_files = git_engine.get_last_commit_diff()

        if not diff_files:
            AuditFormatter.print_info(
                "Tidak ada file yang diubah atau baru di-commit untuk di-audit."
            )
            return

        AuditFormatter.print_info(
            f"Ditemukan {len(diff_files)} file yang perlu di-audit.\n"
        )

        for item in diff_files:
            AuditFormatter.print_info(f"==> Mengaudit File: {item['file_path']}")
            report = auditor.audit_source_code(
                source_code=item["patch"], file_name=item["file_path"]
            )
            AuditFormatter.print_section(f"AUDIT REPORT: {item['file_path']}", report)

    except KeyboardInterrupt:
        print("\n")
        AuditFormatter.print_error("Proses audit dihentikan oleh pengguna (Ctrl+C).")
        sys.exit(0)
    except Exception as err:
        AuditFormatter.print_error(f"Eksekusi Audit Gagal: {str(err)}")


if __name__ == "__main__":
    main()
