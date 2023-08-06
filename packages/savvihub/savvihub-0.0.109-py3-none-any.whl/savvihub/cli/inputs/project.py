import inquirer
import typer

from savvihub.api.exceptions import NotFoundAPIException
from savvihub.cli.constants import PROJECT_TYPE_CLI_DRIVEN
from savvihub.cli.exceptions import ExitException, InvalidGitRepository
from savvihub.cli.git import GitRepository
from savvihub.cli.typer import Context


def eval_project_type(project, project_type: str) -> bool:
    if project.type != project_type:
        raise ExitException(f'Project `{project.name}` type `{project.type}` does not match with `{project_type}`')
    return True

def project_name_callback(ctx: Context, project_name: str) -> str:
    workspace_name = ctx.params['workspace_name']
    try:
        git_repo = GitRepository()
        owner, repo_name, _ = git_repo._get_github_repo()
        if project_name:
            try:
                ctx.project = ctx.authenticated_client.project_read(workspace_name, project_name)
            except NotFoundAPIException:
                raise ExitException(f'Project `{project_name}` does not exist in the workspace `{workspace_name}`.')

            if ctx.project.cached_git_owner_slug == owner and ctx.project.cached_git_repo_slug == repo_name:
                ctx.git_repo = git_repo
        else:
            projects = ctx.authenticated_client.project_list(workspace_name).results
            matched_projects = []
            for project in projects:
                if project.cached_git_owner_slug == owner and project.cached_git_repo_slug == repo_name:
                    matched_projects.append(project)
            if len(matched_projects) == 1:
                ctx.project = matched_projects[0]
                ctx.git_repo = git_repo
            elif len(matched_projects) > 1:
                ctx.project = inquirer.prompt([inquirer.List(
                    'project',
                    message='Select project',
                    choices=[(p.name, p) for p in matched_projects],
                )]).get('project')
                ctx.git_repo = git_repo
            else:
                ctx.project = inquirer.prompt([inquirer.List(
                    'project',
                    message='Select project',
                    choices=[(p.name, p) for p in projects],
                )]).get('project')

        return ctx.project.name

    except InvalidGitRepository:
        if project_name:
            try:
                project = ctx.authenticated_client.project_read(workspace_name, project_name)
                if eval_project_type(project, PROJECT_TYPE_CLI_DRIVEN):
                    ctx.project = project
            except NotFoundAPIException:
                raise ExitException(f'Project `{project_name}` does not exist in the workspace `{workspace_name}`.')
            return project_name
        else:
            projects = ctx.authenticated_client.project_list(workspace_name).results
            if not projects:
                raise ExitException(f'No project found in workspace `{workspace_name}`')

            if len(projects) == 1:
                project = projects[0]
                if eval_project_type(project, PROJECT_TYPE_CLI_DRIVEN):
                    ctx.project = project
            else:
                project = inquirer.prompt([inquirer.List(
                    'project',
                    message='Select project',
                    choices=[(p.name, p) for p in projects],
                )]).get('project')
                if eval_project_type(project, PROJECT_TYPE_CLI_DRIVEN):
                    ctx.project = project
            return ctx.project.name


project_name_option = typer.Option(None, '--project', callback=project_name_callback,
                                   help='If not present, uses git repository name of the current directory.')
