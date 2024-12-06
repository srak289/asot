from ipaddress import IPv4Address, IPv4Network
from sqlalchemy.orm import (
    declared_attr,
    Mapped,
    mapped_column,
    DeclarativeBase,
    MappedAsDataclass,
)


class Base(MappedAsDataclass, DeclarativeBase):
    id: Mapped[int] = mapped_column(init=False, primary_key=True)

class ElasticIPv4Address(Base):
    __tablename__ = "elastic_ipv4"
    """Represent a public address allocation
    """
    allocation_id: Mapped[str] = mapped_column(unique=True)
    association_id: Mapped[str] = mapped_column(nullable=True)
    tags: Mapped[str] = mapped_column(nullable=True)

# class ElasticMachine(Base):
#     __tablename__ = "elastic_machine"
#     """Represent a public-facing machine to accept VPN clients
#     """
#     instance_id: Mapped[str] = mapped_column(unique=True)
#     tags: Mapped[str] = mapped_column(nullable=True)
# 
# class ElasticInterface(Base):
#     __tablename__ = "elastic_interface"
#     """Represent an AWS EC2 ENI attached to a :class:`Machine`
#     """
#     eni_id: Mapped[str] = mapped_column(unique=True)
#     tags: Mapped[str] = mapped_column(nullable=True)
#     region: Mapped[str] = mapped_column(nullable=True)
#     description: Mapped[str] = mapped_column(nullable=True)
#     ipv4addresses: Mapped[List[IPv4Address] | None] = mapped_column(nullable=True)
#     ipv4prefixes: Mapped[List[IPv4Address] | None] = mapped_column(nullable=True)


# One network per tunnel interface
class WireguardNetwork(Base):
    __tablename__ = "wireguard_network"

    ipv4network: Mapped[IPv4Network]

    # wireguard_endpoint_id: Mapped[int] = mapped_column(ForeignKey("wireguard_endpoint.id"))
    # interface: Mapped["WireguardInterface"] = relationship("wireguard_endpoint", back_populates="interface")

class WireguardEndpoint(Base):
    __tablename__ = "wireguard_endpoint"

    ipv4address: Mapped[IPv4Address]
    public_key: Mapped[str] = mapped_column(unique=True)
    listen_port: Mapped[int] = mapped_column(nullable=True) # only on server
    allowed_ips: Mapped[List[IPv4Address]] = mapped_column(nullable=True)

    wireguard_network_id: Mapped[int] = mapped_column(ForeignKey())

class IPv4AddressMap(Base):
    elastic_ipv4address_id: Mapped[int] = mapped_column(ForeignKey())
    wireguard_endpoint_id: Mapped[int] = mapped_column(ForeignKey())
