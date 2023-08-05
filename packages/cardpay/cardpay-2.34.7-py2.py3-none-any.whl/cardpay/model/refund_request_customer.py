# coding: utf-8

"""
    CardPay REST API

    Welcome to the CardPay REST API. The CardPay API uses HTTP verbs and a [REST](https://en.wikipedia.org/wiki/Representational_state_transfer) resources endpoint structure (see more info about REST). Request and response payloads are formatted as JSON. Merchant uses API to create payments, refunds, payouts or recurrings, check or update transaction status and get information about created transactions. In API authentication process based on [OAuth 2.0](https://oauth.net/2/) standard. For recent changes see changelog section.  # noqa: E501

    OpenAPI spec version: 3.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class RefundRequestCustomer(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {"email": "str", "full_name": "str", "identity": "str"}

    attribute_map = {"email": "email", "full_name": "full_name", "identity": "identity"}

    def __init__(self, email=None, full_name=None, identity=None):  # noqa: E501
        """RefundRequestCustomer - a model defined in Swagger"""  # noqa: E501

        self._email = None
        self._full_name = None
        self._identity = None
        self.discriminator = None

        if email is not None:
            self.email = email
        if full_name is not None:
            self.full_name = full_name
        if identity is not None:
            self.identity = identity

    @property
    def email(self):
        """Gets the email of this RefundRequestCustomer.  # noqa: E501

        Customer email address. Mandatory for BOLETO, LOTERICA, DEPOSITEXPRESSBRL.  # noqa: E501

        :return: The email of this RefundRequestCustomer.  # noqa: E501
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email):
        """Sets the email of this RefundRequestCustomer.

        Customer email address. Mandatory for BOLETO, LOTERICA, DEPOSITEXPRESSBRL.  # noqa: E501

        :param email: The email of this RefundRequestCustomer.  # noqa: E501
        :type: str
        """
        if email is not None and len(email) > 256:
            raise ValueError(
                "Invalid value for `email`, length must be less than or equal to `256`"
            )  # noqa: E501
        if email is not None and len(email) < 1:
            raise ValueError(
                "Invalid value for `email`, length must be greater than or equal to `1`"
            )  # noqa: E501

        self._email = email

    @property
    def full_name(self):
        """Gets the full_name of this RefundRequestCustomer.  # noqa: E501

        Customer full name. Mandatory for BOLETO, LOTERICA, DEPOSITEXPRESSBRL.  # noqa: E501

        :return: The full_name of this RefundRequestCustomer.  # noqa: E501
        :rtype: str
        """
        return self._full_name

    @full_name.setter
    def full_name(self, full_name):
        """Sets the full_name of this RefundRequestCustomer.

        Customer full name. Mandatory for BOLETO, LOTERICA, DEPOSITEXPRESSBRL.  # noqa: E501

        :param full_name: The full_name of this RefundRequestCustomer.  # noqa: E501
        :type: str
        """
        if full_name is not None and len(full_name) > 256:
            raise ValueError(
                "Invalid value for `full_name`, length must be less than or equal to `256`"
            )  # noqa: E501
        if full_name is not None and len(full_name) < 1:
            raise ValueError(
                "Invalid value for `full_name`, length must be greater than or equal to `1`"
            )  # noqa: E501

        self._full_name = full_name

    @property
    def identity(self):
        """Gets the identity of this RefundRequestCustomer.  # noqa: E501

        Customer identity for Latin America - Customer’s personal identification number: 'CPF' or 'CNPJ' for Brazil. Mandatory for BOLETO, LOTERICA, DEPOSITEXPRESSBRL.  # noqa: E501

        :return: The identity of this RefundRequestCustomer.  # noqa: E501
        :rtype: str
        """
        return self._identity

    @identity.setter
    def identity(self, identity):
        """Sets the identity of this RefundRequestCustomer.

        Customer identity for Latin America - Customer’s personal identification number: 'CPF' or 'CNPJ' for Brazil. Mandatory for BOLETO, LOTERICA, DEPOSITEXPRESSBRL.  # noqa: E501

        :param identity: The identity of this RefundRequestCustomer.  # noqa: E501
        :type: str
        """
        if identity is not None and len(identity) > 256:
            raise ValueError(
                "Invalid value for `identity`, length must be less than or equal to `256`"
            )  # noqa: E501
        if identity is not None and len(identity) < 0:
            raise ValueError(
                "Invalid value for `identity`, length must be greater than or equal to `0`"
            )  # noqa: E501

        self._identity = identity

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(
                    map(lambda x: x.to_dict() if hasattr(x, "to_dict") else x, value)
                )
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(
                    map(
                        lambda item: (item[0], item[1].to_dict())
                        if hasattr(item[1], "to_dict")
                        else item,
                        value.items(),
                    )
                )
            else:
                if value is not None:
                    result[attr] = value
        if issubclass(RefundRequestCustomer, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, RefundRequestCustomer):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
