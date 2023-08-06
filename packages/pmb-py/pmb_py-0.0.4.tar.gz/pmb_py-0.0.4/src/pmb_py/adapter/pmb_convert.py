from pmb_py.domain import model


def to_project_status(item):
    return model.PmbProjectStatus(item['id'], item['name'], item['colorCode'], item['code'], item['colorText'])


def to_project_type(item):
    return model.PmbProjectType(item['id'], item['name'])


def to_member_status(item):
    return model.PmbMemberStatus(item['id'], item['name'], item['codeName'])


def to_project(item):
    return model.PmbProject(item['id'], item['name'], item['typeId'], item['code'])


# def to_pmb_task(item):
#     return model.


def to_pmb_block(item):
    return model.PmbBlock(item['id'], item['date'], item['duration'], item['task_id'], item['member_id'], item['project_id'], item['type_id'])


def to_ganttitem(item):
    return model.PmbGanttItem(
        item.get('id', 0),
        item.get('name', ''),
        item.get('task_type', 0),
        item.get('status', None),
        item.get('start_datetime', None),
        item.get('end_datetime', None),
        item.get('parent_id', 0),
        item.get('sg_task_id', 0),
        item.get('project_id',0),
        item.get('legend', ''),
        item.get('read_only', 1)
    )
