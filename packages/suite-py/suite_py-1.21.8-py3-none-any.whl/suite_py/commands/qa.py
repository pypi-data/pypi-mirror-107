# -*- coding: utf-8 -*-

import sys
import json

from rich.table import Table
from rich.console import Console
from suite_py.lib import logger
from suite_py.lib.handler import prompt_utils
from suite_py.lib.handler.qainit_handler import QainitHandler
from suite_py.lib.handler import git_handler as git
from suite_py.lib.handler.git_handler import GitHandler


class QA:
    def __init__(self, action, project, config, tokens, flags=None):
        self._action = action
        self._project = project
        self._flags = flags
        self._config = config
        self._tokens = tokens
        self._git = GitHandler(project, config)
        self._qainit = QainitHandler(project, config, tokens)

    def run(self):
        if self._action == "list":
            self._list()
        elif self._action == "create":
            self._create()
        elif self._action == "update":
            self._update()
        elif self._action == "delete":
            self._delete()
        elif self._action == "check":
            self._check()
        elif self._action == "describe":
            self._describe()
        elif self._action == "update-quota":
            self._update_quota()

    def _check(self):
        r = self._qainit.execute("GET", "/api/v1/user")
        logger.info(
            "Checking configuration. If there is an issue, check ~/.suite_py/config.yml file and execute: suite-py login"
        )
        logger.debug(json.dumps(r.json(), indent=2))

    def _list(self):
        if self._flags:
            self._list_others(self._flags)
            return

        table = Table()
        table.add_column("Name", style="purple")
        table.add_column("Hash", style="green")
        table.add_column("Created by", style="white")
        table.add_column("Updated by", style="white")
        table.add_column("Deleted by", style="white")
        table.add_column("Status", style="white")
        console = Console()

        r = self._qainit.execute("GET", "/api/v1/qa")

        qa_list = r.json()["list"]
        for qa in qa_list:
            table.add_row(
                qa["name"],
                qa["hash"],
                qa.get("created", {}).get("github_username", "/")
                if qa["created"] is not None
                else "/",
                qa.get("updated", {}).get("github_username", "/")
                if qa["updated"] is not None
                else "/",
                qa.get("deleted", {}).get("github_username", "/")
                if qa["deleted"] is not None
                else "/",
                qa["status"],
            )
        console.print(table)

    def _list_others(self, user):
        table = Table()
        table.add_column("Name", style="purple")
        table.add_column("Hash", style="green")
        table.add_column("Created by", style="white")
        table.add_column("Updated by", style="white")
        table.add_column("Deleted by", style="white")
        table.add_column("Status", style="white")
        console = Console()
        r = self._qainit.execute("GET", f"/api/v1/qa?user={user}")

        qa_list = r.json()["list"]
        for qa in qa_list:
            table.add_row(
                qa["name"],
                qa["hash"],
                qa.get("created", {}).get("github_username", "/")
                if qa["created"] is not None
                else "/",
                qa.get("updated", {}).get("github_username", "/")
                if qa["updated"] is not None
                else "/",
                qa.get("deleted", {}).get("github_username", "/")
                if qa["deleted"] is not None
                else "/",
                qa["status"],
            )
        console.print(table)

    def _describe(self):
        qa_hash = self._flags["qa_hash"]
        jsonify = self._flags["json"]

        table = Table()
        table.add_column("Microservice", style="purple", no_wrap=True)
        table.add_column("Branch", style="green")
        table.add_column("Drone build")
        table.add_column("Status", style="white")
        console = Console()

        r = self._qainit.execute(
            "GET",
            f"/api/v1/qa/{qa_hash}",
        )
        try:
            resources_list = r.json()["list"]["resources"]
            for resource in resources_list:
                if resource["type"] == "microservice":
                    drone_url = (
                        "[blue][u]"
                        + "https://drone-1.prima.it/primait/"
                        + resource["name"]
                        + "/"
                        + resource["promoted_build"]
                        + "[/u][/blue]"
                    )
                    table.add_row(
                        resource["name"],
                        resource["ref"],
                        drone_url,
                        resource["status"],
                    )
            if jsonify:
                print(json.dumps(r.json(), indent=2))
            else:
                print(
                    f"""
> Prima url: https://www-{qa_hash}.prima.qa
> Backoffice (Borat) url: https://backoffice-{qa_hash}.prima.qa
> Urania url: http://urania-{qa_hash}.prima.qa
> Bburago url: http://bburago-{qa_hash}.prima.qa
> Ermes url: http://ermes-{qa_hash}.prima.qa
> Hal9000 url: http://hal9000{qa_hash}.prima.qa
> Fidaty url: http://fidaty-{qa_hash}.prima.qa
> Peano url: http://peano-{qa_hash}.prima.qa
> Assange url: https://assange-{qa_hash}.prima.qa
> Activia url: http://activia-{qa_hash}.prima.qa
> Skynet url: http://skynet-{qa_hash}.prima.qa
> Roger url: http://roger-{qa_hash}.prima.qa
> Leftorium url: http://leftoriu-{qa_hash}.prima.qa
> Rachele url: http://rachele-{qa_hash}.prima.qa
> Maia App url: https://api-{qa_hash}.prima.qa
> Maia Intermediari url: https://api-intermediari-{qa_hash}.prima.qa
> Maia Casa url: https://api-casa-{qa_hash}.prima.qa
> Maia Pagamenti url: https://api-pagamenti-{qa_hash}.prima.qa
> Maia Sostituzioni url: https://api-sostituzioni-{qa_hash}.prima.qa
> Legion url: http://legion-{qa_hash}.prima.qa
> Crash url: https://crash-{qa_hash}.prima.qa
> Starsky url: https://starsky-{qa_hash}.prima.qa
> Hutch url: https://hutch-{qa_hash}.prima.qa
> Vianello url: https://vianello-{qa_hash}.prima.qa
> Domus url: https://domus-{qa_hash}.prima.qa
> Lira url: https://lira-{qa_hash}.prima.qa
> Baggio url: https://baggio-{qa_hash}.prima.qa
> Mario url: https://mario-{qa_hash}.prima.qa
> Mario Backend url: https://api-mario-{qa_hash}.prima.qa
> Zuhause url: https://zuhause-{qa_hash}.prima.qa
> Pyxis url: https://pyxis-{qa_hash}.prima.qa
> Caritas url: https://caritas-{qa_hash}.prima.qa
> Cashabck url: https://cashback-{qa_hash}.prima.qa
> Evvivass url: https://evvivass-{qa_hash}.prima.qa
                """
                )
                console.print(table)
        except TypeError:
            logger.error("Wrong hash")

    def _delete(self):
        qa_hash = self._flags

        r = self._qainit.execute(
            "DELETE",
            f"/api/v1/qa/{qa_hash}",
        )
        logger.info("QA deletion initiated")
        logger.debug(json.dumps(r.json(), indent=2))

    def _create(self):
        r = self._qainit.execute("GET", "/api/v1/user")
        r = r.json()
        if not r["quota"]["remaining"] > 0:
            logger.error("There's no remaining quota for you.")
            sys.exit("-1")
        if "staging" in self._qainit.url:
            qa_default_name = (
                f"staging_{git.get_username()}_{self._git.current_branch_name()}"
            )
        else:
            qa_default_name = f"{git.get_username()}_{self._git.current_branch_name()}"

        qa_name = prompt_utils.ask_questions_input(
            "Choose the QA name: ", default_text=qa_default_name
        )

        srv_list = self._qainit.create_services_body(prj_list=self._flags)

        body = {"name": f"{qa_name}", "services": srv_list}
        logger.debug(json.dumps(body))
        r = self._qainit.execute(
            "POST",
            "/api/v1/qa",
            body=json.dumps(body),
        )
        logger.info("QA creation initiated. Your namespace hash: ")
        logger.info(r.json()["hash"])
        logger.debug(json.dumps(r.json(), indent=2))

    def _update(self):
        qa_hash = self._flags[0]
        prj_list = self._flags[1:]

        srv_list = self._qainit.create_services_body(prj_list)

        body = {"services": srv_list}
        logger.debug(json.dumps(body))
        r = self._qainit.execute(
            "PUT",
            f"/api/v1/qa/{qa_hash}",
            body=json.dumps(body),
        )
        logger.info("QA update initiated")
        logger.debug(json.dumps(r.json(), indent=2))

    def _update_quota(self):
        username = prompt_utils.ask_questions_input("Insert GitHub username: ")
        quota = prompt_utils.ask_questions_input("Insert new quota value: ")

        body = {"github_username": f"{username}", "quota": f"{quota}"}
        logger.debug(json.dumps(body))
        r = self._qainit.execute(
            "POST",
            "/api/v1/user/quota",
            body=json.dumps(body),
        )

        logger.info("Quota updated.")
        logger.debug(json.dumps(r.json(), indent=2))
