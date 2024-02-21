# Mixin for nested viewsets


class NestedViewSetMixin:
    # special properties
    _action = "root"
    _curr_action = None
    _nested_detail = False
    root_obj_name = "instance"

    # Dynamic method patterns
    BASE_QS_PAT = "%s_base_qs"
    QS_PAT = "%s_queryset"
    LOOKUP_PAT = "set_%s_lookup"
    OBJ_PAT = "%s_object"
    SER_PAT = "%s_serializer"
    SER_CLASS_PAT = "%s_ser_class"
    SER_KWARGS_PAT = "%s_ser_kwargs"
    CREATE_PAT = "%s_create"
    UPDATE_PAT = "%s_update"
    DESTROY_PAT = "%s_destroy"

    @property
    def root_action(self):
        return type(self)._action

    @property
    def is_nested(self):
        return self.root_action != self._action

    @property
    def nested_detail(self):
        return getattr(self, "_nested_detail", False)

    @property
    def no_current(self):
        return self._curr_action is None

    @property
    def is_root(self):
        return self.root_action == self._action

    def dynamic_call(self, pat: str, default, *args, **kwargs):
        action = self._curr_action or self.root_action
        return getattr(self, pat % action, default)(*args, **kwargs)

    def _base_qs_dispatch(self):
        default = getattr(self, self.QS_PAT % self.root_action, super().get_queryset)
        return getattr(self, self.BASE_QS_PAT % self._action, default)()

    def set_def_lookup(self):
        self.lookup_field = "pk"
        self.lookup_url_kwarg = "pk"

    def set_nested_lookup(self):
        if self.is_nested:
            self.dynamic_call(self.LOOKUP_PAT, self.set_def_lookup)

    def get_queryset(self):
        if self.is_nested and self.no_current:
            return self._base_qs_dispatch()
        return self.dynamic_call(self.QS_PAT, super().get_queryset)

    def get_object(self):
        return self.dynamic_call(self.OBJ_PAT, super().get_object)

    def get_serializer_class(self):
        return self.dynamic_call(self.SER_CLASS_PAT, super().get_serializer_class)

    def get_serializer(self, *args, **kwargs):
        try:
            kwargs.update(getattr(self, self.SER_KWARGS_PAT % self._curr_action)())
        except AttributeError:
            pass
        return self.dynamic_call(self.SER_PAT, super().get_serializer, *args, **kwargs)

    def perform_create(self, serializer):
        self.dynamic_call(self.CREATE_PAT, super().perform_create, serializer)

    def perform_update(self, serializer):
        self.dynamic_call(self.UPDATE_PAT, super().perform_update, serializer)

    def perform_destroy(self, instance):
        self.dynamic_call(self.DESTROY_PAT, super().perform_destroy, instance)

    def get_root_pk(self):
        return self.kwargs[self.lookup_url_kwarg]
