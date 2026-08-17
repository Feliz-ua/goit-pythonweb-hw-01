import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class VehicleSpec:
    make: str
    model: str
    region: str

    def __str__(self) -> str:
        return f"{self.make} {self.model} ({self.region})"


class Vehicle(ABC):
    def __init__(self, spec: VehicleSpec) -> None:
        self.spec = spec

    @abstractmethod
    def start_engine(self) -> None:
        """Запускає двигун транспортного засобу."""


class Car(Vehicle):
    # Реалізація автомобіля.
    def start_engine(self) -> None:
        logger.info("%s: Двигун запущено", self.spec)


class Motorcycle(Vehicle):
    # Реалізація мотоцикла.

    def start_engine(self) -> None:
        logger.info("%s: Мотор заведено", self.spec)


class VehicleFactory(ABC):
    # Фабрика для транспортних засобів."""

    @abstractmethod
    def create_car(self, make: str, model: str) -> Car:
        """Створює автомобіль."""

    @abstractmethod
    def create_motorcycle(self, make: str, model: str) -> Motorcycle:
        """Створює мотоцикл."""


class USVehicleFactory(VehicleFactory):
    # Фабрика для транспортних засобів американської специфікації.

    REGION = "US Spec"

    def create_car(self, make: str, model: str) -> Car:
        spec = VehicleSpec(make=make, model=model, region=self.REGION)
        return Car(spec)

    def create_motorcycle(self, make: str, model: str) -> Motorcycle:
        spec = VehicleSpec(make=make, model=model, region=self.REGION)
        return Motorcycle(spec)


class EUVehicleFactory(VehicleFactory):
    # Фабрика для транспортних засобів європейської специфікації.

    REGION = "EU Spec"

    def create_car(self, make: str, model: str) -> Car:
        spec = VehicleSpec(make=make, model=model, region=self.REGION)
        return Car(spec)

    def create_motorcycle(self, make: str, model: str) -> Motorcycle:
        spec = VehicleSpec(make=make, model=model, region=self.REGION)
        return Motorcycle(spec)


def demo_factories() -> None:
    logger.info("=== Демонстрація фабрик ===")

    us_factory = USVehicleFactory()
    us_car = us_factory.create_car("Ford", "Focus")
    us_motorcycle = us_factory.create_motorcycle("Indian", "Scout")

    us_car.start_engine()
    us_motorcycle.start_engine()

    eu_factory = EUVehicleFactory()
    eu_car = eu_factory.create_car("Skoda", "Superb")
    eu_motorcycle = eu_factory.create_motorcycle("Ducati", "Panigale")

    eu_car.start_engine()
    eu_motorcycle.start_engine()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    demo_factories()
