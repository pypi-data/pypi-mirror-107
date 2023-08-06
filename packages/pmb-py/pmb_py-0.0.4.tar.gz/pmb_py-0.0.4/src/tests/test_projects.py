import pmb_py


def test_list_projects(pmb):
    projects = pmb.api.PmbProjects.list()
    for project in projects:
        assert type(project) == pmb_py.domain.model.PmbProject