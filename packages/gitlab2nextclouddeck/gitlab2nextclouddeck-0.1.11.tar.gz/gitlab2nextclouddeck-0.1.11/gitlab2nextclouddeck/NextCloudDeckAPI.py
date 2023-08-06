import requests
import random
from progress.bar import ShadyBar


class NextCloudDeckAPI:
    """docstring for NextCloudDeck."""

    def __init__(self, url, auth):
        self.url = url
        self.auth = auth
        self.headers = {"OCS-APIRequest": "true", "Content-Type": "application/json"}

    def getBoards(self):
        response = requests.get(
            f"{self.url}/index.php/apps/deck/api/v1.0/boards",
            auth=self.auth,
            headers=self.headers,
        )
        response.raise_for_status()
        # return response.json()
        boards_list = []
        for board in response.json():
            boards_list.append(board["title"] + "::" + str(board["id"]))
        return boards_list

    def getBoardsFull(self, boardId):
        response = requests.get(
            f"{self.url}/index.php/apps/deck/api/v1.0/boards/{boardId}",
            auth=self.auth,
            headers=self.headers,
        )
        response.raise_for_status()
        return response.json()

    def getStacks(self, boardId):
        response = requests.get(
            f"{self.url}/index.php/apps/deck/api/v1.0/boards/{boardId}/stacks",
            auth=self.auth,
            headers=self.headers,
        )
        response.raise_for_status()
        # return response.json()
        stack_list = []
        for board in response.json():
            stack_list.append(board["title"] + "::" + str(board["id"]))
        return stack_list

    def getCardsFromStack(self, boardId, stackId):
        response = requests.get(
            f"{self.url}/index.php/apps/deck/api/v1.0/boards/{boardId}/stacks/{stackId}",
            auth=self.auth,
            headers=self.headers,
        )
        response.raise_for_status()
        if "cards" in response.json():
            return response.json()["cards"]
        return []

    def getCard(self, boardId, stackId, cardId):
        response = requests.get(
            f"{self.url}/index.php/apps/deck/api/v1.0/boards/{boardId}/stacks/{stackId}/cards/{cardId}",
            auth=self.auth,
            headers=self.headers,
        )
        response.raise_for_status()

        return response.json()

    def createLabel(self, title, color, boardId):
        response = requests.post(
            f"{self.url}/index.php/apps/deck/api/v1.0/boards/{boardId}/labels",
            auth=self.auth,
            json={"title": title, "color": color},
            headers=self.headers,
        )
        response.raise_for_status()
        return response.json()

    def createStack(self, title, order, boardId):
        response = requests.post(
            f"{self.url}/index.php/apps/deck/api/v1.0/boards/{boardId}/stacks",
            auth=self.auth,
            json={"title": title, "order": order},
            headers=self.headers,
        )
        response.raise_for_status()
        return response.json()

    def createCard(self, title, ctype, order, description, duedate, boardId, stackId):
        response = requests.post(
            f"{self.url}/index.php/apps/deck/api/v1.0/boards/{boardId}/stacks/{stackId}/cards",
            auth=self.auth,
            json={
                "title": title,
                "type": ctype,
                "order": order,
                "description": description,
                "duedate": duedate,
            },
            headers=self.headers,
        )
        response.raise_for_status()
        return response.json()

    def updateCard(
        self,
        title="",
        description="",
        duedate=None,
        boardId=None,
        stackId=None,
        cardId=None,
    ):
        response = requests.put(
            f"{self.url}/index.php/apps/deck/api/v1.0/boards/{boardId}/stacks/{stackId}/cards/{cardId}",
            auth=self.auth,
            json={
                "title": title,
                "type": "plain",
                "order": None,
                "description": description,
                "duedate": duedate,
                "owner": "fecub",
            },
            headers=self.headers,
        )

        # print(response.content)
        response.raise_for_status()
        return response.json()

    def deleteAllCardsStack(self, boardId=None, stackId=None):
        cardId = ""

        cards = self.getCardsFromStack(boardId, stackId)
        bar = ShadyBar("Delete Items", max=len(cards))
        response = None
        for card in cards:
            response = requests.delete(
                f'{self.url}/index.php/apps/deck/api/v1.0/boards/{boardId}/stacks/{stackId}/cards/{card["id"]}',
                auth=self.auth,
                headers=self.headers,
            )
            response.raise_for_status()
            bar.next()
        bar.finish()
        if response is not None:
            return response.json()
        else:
            return

    def getLabels(self, boardId):
        boards = self.getBoardsFull(boardId)
        return boards["labels"]

    def create_non_exists_label(self, glbLabels, board_id):
        def r():
            return random.randint(0, 255)

        hex_color = "%02X%02X%02X" % (r(), r(), r())
        ncdLabels = self.getLabels(int(board_id))

        break_out_flag = False
        for glbLabel in glbLabels:
            for ncdLabel in ncdLabels:
                if glbLabel in ncdLabel["title"]:
                    break_out_flag = True
                    break
            if break_out_flag:
                break
            self.createLabel(glbLabel, hex_color, board_id)
            ncdLabels = self.getLabels(int(board_id))

    def assignLabel(self, labelId, cardId, boardId, stackId):
        response = requests.put(
            f"{self.url}/index.php/apps/deck/api/v1.0/boards/{boardId}/stacks/{stackId}/cards/{cardId}/assignLabel",
            auth=self.auth,
            json={"labelId": labelId},
            headers=self.headers,
        )
        response.raise_for_status()

    def assignAllLabels(self, glbLabels, card_id, board_id, stack_id):
        ncdLabels = self.getLabels(board_id)

        for glbLabel in glbLabels:
            for ncdLabel in ncdLabels:
                if glbLabel in ncdLabel["title"]:
                    self.assignLabel(int(ncdLabel["id"]), card_id, board_id, stack_id)

    def assignLinkedIssues(
        self,
        title,
        duedate,
        desc,
        board_id,
        stack_id,
        card_id,
        glbLinkIssues,
        existent_desc,
    ):
        issues_desc = ""
        for glbLinkIssue in glbLinkIssues:
            glbtitle = glbLinkIssue.split("::")[0]
            id = glbLinkIssue.split("::")[1]
            check = glbLinkIssue.split("::")[2]
            web_url = glbLinkIssue.split("::")[3]

            checked = "x" if check == "✔️" else " "
            issues_desc = issues_desc + f"- [{checked}] #{id} {glbtitle}\n"

        linked_issues_desc = desc + f"\n\n### Verlinkte Tickets:\n\n{issues_desc}"
        existent_desc = existent_desc + linked_issues_desc
        self.updateCard(
            title=title,
            description=linked_issues_desc,
            duedate=duedate,
            boardId=board_id,
            stackId=stack_id,
            cardId=card_id,
        )

    def output_stacks(self, stacks):
        x = PrettyTable()
        x.field_names = ["#", "Title", "ID"]
        for num, stack in enumerate(stacks, start=0):
            x.add_row([num, stack["title"], stack["id"]])
        print(x)
        return x
