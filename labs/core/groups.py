class GROUPS:
    USER_GROUP = "User"

    _USER_GROUP_CODENAMES = [
        # project
        "view_project",
        "add_project",
        "change_project",
        "delete_project",
        # prompt
        "view_prompt",
        "change_prompt",
        "delete_prompt",
        # vectorizer
        "view_vectorizer",
        "change_vectorizer",
        "delete_vectorizer",
        # workflow result
        "view_workflowresult",
        "delete_workflowresult",
    ]

    @classmethod
    def as_list(cls) -> list:
        # return class properties if they do not contain "__", "object_at" or is not methods
        return [
            v
            for k, v in cls.__dict__.items()
            if not any(map(lambda s: s in k, ["__", "object_at"]))
            and not callable(getattr(cls, k))
            and not isinstance(v, list)
        ]

    @classmethod
    def get_group_permission_codenames(cls, group_name: str):
        match group_name:
            case cls.USER_GROUP:
                codenames = cls._USER_GROUP_CODENAMES

            case _:
                raise ValueError(f"Invalid group name. Valid groups names are {', '.join(cls.as_list())}")

        return codenames
