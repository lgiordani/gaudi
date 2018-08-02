from gaudi import domain_model


def test_domain_model_instance():
    class MyModel:
        pass

    domain_model.DomainModel.register(MyModel)

    assert issubclass(MyModel, domain_model.DomainModel)
