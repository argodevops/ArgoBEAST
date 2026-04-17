import os
import shutil
import subprocess
import logging
from argo_beast.behave_integration.behave_helpers import (
    cleanup_results,
    DummyStreamOpener,
)
from argo_beast.cli.helpers import ensure_dir


class ReportManager:
    def __init__(self, context):
        self.context = context
        self.config = context.beast_config
        self.allure_dir = "allure-results"
        self.report_dir = "allure-report"
        self.is_enabled = self.config.get("allure_reporting", False)

    def setup_reporting(self):
        if not self.is_enabled:
            return
        try:
            # pylint: disable=import-outside-toplevel
            from allure_behave.formatter import AllureFormatter
        except ImportError as exc:
            raise ImportError("allure-behave is not installed.") from exc

        if os.path.exists(self.allure_dir):
            shutil.rmtree(self.allure_dir)
        ensure_dir(self.allure_dir)

        hide_excluded = self.config.get("hide_excluded_tests", False)
        self.context.config.userdata["AllureFormatter.hide_excluded"] = str(
            hide_excluded
        ).lower()

        allure_formatter = AllureFormatter(
            DummyStreamOpener(self.allure_dir), self.context.config
        )
        self.context._runner.formatters.append(allure_formatter)  # pylint: disable=protected-access

    def finalise_reporting(self):
        if not self.is_enabled:
            return

        if self.context.beast_config.get("allure_keep_history"):
            if os.path.exists(f"{self.report_dir}/history"):
                shutil.copytree(
                    f"{self.report_dir}/history", f"{self.allure_dir}/history"
                )

        cleanup_results(self.allure_dir, self.config.get("hide_skipped_tests", False))

        if self.config.get("auto_generate_report", True):
            self._run_cli()

    def _run_cli(self):
        try:
            subprocess.run(
                [
                    "allure",
                    "generate",
                    self.allure_dir,
                    "-o",
                    self.report_dir,
                    "--clean",
                ],
                check=True,
            )
            logging.info(f"Allure report generated at: {self.report_dir}")
            shutil.make_archive("allure-report", "zip", self.report_dir)
        except FileNotFoundError:
            logging.warning("Allure CLI not found in PATH. Generation skipped.")
        except Exception as e:
            logging.error(f"Report generation failed: {e}")
