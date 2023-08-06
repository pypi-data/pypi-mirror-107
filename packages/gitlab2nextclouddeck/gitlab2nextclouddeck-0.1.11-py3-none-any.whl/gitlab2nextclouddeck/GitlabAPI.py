from gitlab import Gitlab


class GitlabAPI:
    """docstring for GitlabAPI."""

    def __init__(self, url, token):
        self.gl = Gitlab(url, token)

    def getProjects(self):
        # list all the projects
        projects = self.gl.projects.list()
        project_list = []
        for project in projects:
            project_list.append(project.name.strip() + "::" + str(project.id))
        return project_list

    def getProject(self, id):
        return self.gl.projects.get(id)

    def getIssues(self, project):
        # list all issues for project
        issues = project.issues.list(state="opened", order_by="created_at", sort="asc")
        return issues

    def getLinkedIssues(self, issue):
        linked_issues = issue.links.list()
        linked_issues_list = []
        for lissue in linked_issues:
            linked_issues_list.append(
                lissue.title.strip()
                + "::"
                + str(lissue.iid)
                + "::"
                + ("✔️" if lissue.state != "opened" else "")
                + "::"
                + lissue.web_url
            )

        return linked_issues_list

    def filter_labels(self, labels):
        black_list_labels = ["In Arbeit", "In Review", "in Warteschleife", "To Do"]
        for bLabel in black_list_labels:
            labels = [label for label in labels if bLabel not in label]

        return labels

    def output_projects(self, projects):
        x = PrettyTable()
        x.field_names = ["#", "Title", "ID"]
        for num, project in enumerate(projects, start=0):
            x.add_row([num, project.name, project.id])
        print(x)
        return x
