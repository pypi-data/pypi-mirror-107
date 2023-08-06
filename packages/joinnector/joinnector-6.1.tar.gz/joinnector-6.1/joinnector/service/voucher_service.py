# pylint: disable=useless-super-delegation

from joinnector.service.base_sdk_service import BaseSDKService


class VoucherService(BaseSDKService):
    def __init__(self, name):
        super().__init__(name)


voucher_service = VoucherService("voucher")
