import tldextract
import zope.interface
from certbot import errors, interfaces
from certbot.plugins import dns_common
from pkb_client.client import PKBClient

DEFAULT_PROPAGATION_SECONDS = 60

ACME_TXT_PREFIX = "_acme-challenge"


@zope.interface.implementer(interfaces.IAuthenticator)
@zope.interface.provider(interfaces.IPluginFactory)
class Authenticator(dns_common.DNSAuthenticator):
    """
    Authenticator class to handle a DNS-01 challenge for Porkbun domains.
    """

    description = "Obtain certificates using a DNS TXT record for Porkbun domains"
    record_ids = dict()

    def __init__(self, *args, **kwargs) -> None:
        super(Authenticator, self).__init__(*args, **kwargs)
        self.credentials = None

    @classmethod
    def add_parser_arguments(cls, add: callable) -> None:
        """
        Add required or optional argument for the cli of certbot.

        :param add: method handling the argument adding to the cli
        """

        super(Authenticator, cls).add_parser_arguments(add, default_propagation_seconds=DEFAULT_PROPAGATION_SECONDS)
        add("credentials", help="Porkbun credentials INI file.")
        add("key", help="Porkbun API key (overwrites credentials file)")
        add("secret", help="Porkbun API key secret (overwrites credentials file)")

    @staticmethod
    def more_info() -> str:
        """
        Get more information about this plugin.
        This method is used by certbot to show more info about this plugin.

        :return: string with more information about this plugin
        """

        return "This plugin configures a DNS TXT record to respond to a DNS-01 challenge using the Porkbun API."

    def _setup_credentials(self) -> None:
        """
        Setup Porkbun key and secret from credentials file.
        """

        # If both cli params are provided we do not need a credentials file
        if self.conf("key") and self.conf("secret"):
            return

        self._configure_file('credentials',
                             'Absolute path to Porkbun credentials INI file')
        dns_common.validate_file_permissions(self.conf('credentials'))
        self.credentials = self._configure_credentials(
            "credentials",
            "Porkbun credentials INI file",
            {
                "key": "Porkbun API key.",
                "secret": "Porkbun API key secret.",
            },
        )

    def _perform(self, domain: str, validation_name: str, validation: str) -> None:
        """
        Add the validation DNS TXT record to the provided Porkbun domain.

        :param domain: the Porkbun domain for which a TXT record will be created
        :param validation_name: the value to validate the dns challenge
        :param validation: the value for the TXT record

        :raise PluginError: if the TXT record can not be set or something goes wrong
        """

        tld = tldextract.TLDExtract(suffix_list_urls=None)

        extracted_domain = tld(domain)

        subdomains = extracted_domain.subdomain
        # remove wildcard from subdomains
        subdomains = subdomains.replace("*.", "")
        subdomains = subdomains.replace("*", "")

        if subdomains:
            name = f"{ACME_TXT_PREFIX}.{subdomains}"
        else:
            name = ACME_TXT_PREFIX

        root_domain = f"{extracted_domain.domain}.{extracted_domain.suffix}"

        try:
            self.record_ids[validation] = self._get_porkbun_client().dns_create(root_domain,
                                                                                "TXT",
                                                                                validation,
                                                                                name=name)
        except Exception as e:
            raise errors.PluginError(e)

    def _cleanup(self, domain: str, validation_name: str, validation: str) -> None:
        """
        Delete the TXT record of the provided Porkbun domain.

        :param domain: the Porkbun domain for which the TXT record will be deleted
        :param validation_name: the value to validate the dns challenge
        :param validation: the value for the TXT record

        :raise PluginError:  if the TXT record can not be deleted or something goes wrong
        """

        tld = tldextract.TLDExtract(suffix_list_urls=None)

        extracted_domain = tld(domain)
        root_domain = f"{extracted_domain.domain}.{extracted_domain.suffix}"

        # get the record id with the TXT record
        record_id = self.record_ids[validation]

        try:
            if not self._get_porkbun_client().dns_delete(root_domain, record_id):
                raise errors.PluginError("TXT for domain {} was not deleted".format(domain))
        except Exception as e:
            raise errors.PluginError(e)

    def _get_porkbun_client(self) -> PKBClient:
        """
        Create a new PKBClient with the provided API key and secret.

        :return: the created PKBClient object
        """

        key = self.conf("key") or self.credentials.conf("key")
        secret = self.conf("secret") or self.credentials.conf("secret")

        return PKBClient(key, secret)
