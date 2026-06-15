from dependency_injector import containers, providers
'''
containers lets you define a container class.
providers lets you define how dependencies are created: singleton, factory, object, configuration, etc.
'''
from sqlalchemy.orm import sessionmaker
'''
sessionmaker creates SQLAlchemy Session objects.
A Session is the unit-of-work object used to talk to the database
'''

from app.core.config import settings
from app.db.database import engine

'''
So the engine represents the DB connection layer.
Then the session factory will use this engine to create DB sessions.
'''

from app.services import (
    book_risk_service,
    book_service,
    client_service,
    collateral_service,
    loan_service,
    position_service,
    scenario_service,
    trade_order_service,
    scenario_run_service
)

def create_session_factory() -> sessionmaker:
    return sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False
    )

class Container(containers.DeclarativeContainer):
    # wiring_config = containers.WiringConfiguration(
    #     packages=[
    #         "app.api",
    #         "app.commands"
    #     ]
    # )

    '''
    This tells dependency_injector where it should look for injection points.
    then Dependency Injector can inject dependencies into those modules.
    '''

    config = providers.Configuration()

    db_session_factory = providers.Singleton(create_session_factory)

    client_service = providers.Object(client_service)
    '''
    means: “inside the container, expose this object under the name client_service.”
    '''
    book_service = providers.Object(book_service)
    collateral_service = providers.Object(collateral_service)
    loan_service = providers.Object(loan_service)
    position_service = providers.Object(position_service)
    scenario_service = providers.Object(scenario_service)
    trade_order_service = providers.Object(trade_order_service)
    book_risk_service = providers.Object(book_risk_service)
    scenario_run_service = providers.Object(scenario_run_service)

container = Container()
container.config.from_dict(
    {
        "database_url": settings.database_url
    }
)