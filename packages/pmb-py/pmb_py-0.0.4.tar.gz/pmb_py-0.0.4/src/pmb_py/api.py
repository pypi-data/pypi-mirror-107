import pmb_py.core as core
from pmb_py import PMB_MEMBER_STATUS, PmbError
from pmb_py.adapter import pmb_convert


class pmb_mixin:
    _cache = dict()
    creator = None

    @classmethod
    def list(cls, *args, **kwargs):
        if kwargs.get("force", False) == False and cls._cache:
            return cls._cache.values()
        items = cls.get_query()
        if cls.creator:
            objects = [cls.creator(item) for item in items]
            cls._cache = {object.id: object for object in objects}
        else:
            cls._cache = {item["id"]: item for item in items}
        return cls._cache.values()

    @classmethod
    def get_query(cls, *args, **kwargs):
        pass

    @classmethod
    def get(cls, **kwargs):
        def _get_kwarg(kw, target, iter):
            for item in iter.values():
                if target == getattr(item, kw):
                    return item
            return None

        if not cls._cache:
            cls.list()
        if kwargs.get("id", None):
            the_id = kwargs.get("id")
            return cls._cache.get(the_id)
        if kwargs.get("name", None):
            the_name = kwargs.get("name", None)
            re = _get_kwarg("name", the_name, cls._cache)
            if re:
                return re
        raise PmbError("no support for these keyword")

    @classmethod
    def create_one(cls, *args, **kwargs):
        return dict()

    @classmethod
    def create(cls, *args, **kwargs):
        item = cls.create_one(*args, **kwargs)
        if cls.creator:
            obj = cls.creator(item)
            cls._cache.update({obj.id: obj})
            return obj
        else:
            cls._cache.update({item["id"]: item})
            return item

    @classmethod
    def update_one(cls, obj_id, **kwargs):
        return dict()

    @classmethod
    def update(cls, obj_id, **kwargs):
        try:
            item = cls.update_one(obj_id, **kwargs)
        except Exception as e:
            print(str(e))
            return False
        if cls.creator:
            obj = cls.creator(item)
            cls._cache.update({obj.id: obj})
            return obj
        else:
            cls._cache.update({item["id"]: item})
            return item


class ProjectStatus(pmb_mixin):
    _cache = None
    creator = pmb_convert.to_project_status

    @classmethod
    def get_query(cls):
        api = "web_project_status_and_types"
        re = core._session.post(api)
        return re["data"]["projectStatus"]


class ProjectType(pmb_mixin):
    _cache = None
    creator = pmb_convert.to_project_type

    @classmethod
    def get_query(cls):
        api = "web_project_status_and_types"
        re = core._session.post(api)
        return re["data"]["projectTypes"]


class MemberStatus(pmb_mixin):
    _cache = None
    creator = pmb_convert.to_member_status

    @classmethod
    def get_query(cls):
        status_list = list()
        for k, v in PMB_MEMBER_STATUS.items():
            status_list.append({"id": v[0], "name": v[1], "codeName": k})
        return status_list


class PmbProjects(pmb_mixin):
    _cache = None
    creator = pmb_convert.to_project

    @classmethod
    def get_query(cls, *args, **kwargs):
        api = "web_projects/list"
        re = core._session.post(api)
        return re["data"]["lists"]


# class PmbTasks(pmb_mixin):
#     _cache = None
#     creator = pmb_convert.to_pmb_task


class PmbBlocks(pmb_mixin):
    _cache = None
    creator = pmb_convert.to_pmb_block

    @classmethod
    def list(cls, **kwargs):
        raise PmbError(
            "PmbBlocks is not support list method, instead, use get(id=) or get (task_id=)"
        )

    @classmethod
    def get_query(cls, *args, **kwargs):
        api = "web_tasks_logs_a_day"

    @classmethod
    def get(cls, **kwargs):
        blocks = list()
        task_id = kwargs.get("task_id")
        if not task_id:
            raise PmbError("task_id is require")
        date_ = kwargs.get("task_id")
        if not date_:
            raise PmbError("date is require")
        data = {}


class GanttItems(pmb_mixin):
    _cache = dict()
    creator = pmb_convert.to_ganttitem
    api = "gantt_items"

    @classmethod
    def create_one(cls, *args, **kwargs):
        gantt = core._session.post(cls.api, data=kwargs)
        return gantt

    @classmethod
    def get_query(cls, *args, **kwargs):
        return core._session.get(cls.api, params=kwargs)

    @classmethod
    def update_one(cls, obj_id, **kwargs):
        update_api = "/".join([cls.api, str(obj_id)])
        return core._session.patch(update_api, data=kwargs)
