from picklejson import Context


def test_context_includes_serializable_object(Person):
    print()
    assert '_Person.1.0.0' in Context()


def test_context_is_singleton():
    context1 = Context()
    context2 = Context()
    assert context1 is context2
