from decimal import Decimal
from types import MappingProxyType


class SalaryService:
    pension_rate = MappingProxyType(
        {
            "not_accumulate": 0,
            "accumulateGradually": Decimal(0.027),
            "accumulate": Decimal(0.03),
        }
    )
    mma = 924
    max_bruto = Decimal(2864.19)

    npd_limit = 747
    npd_bruto_limit = 2167

    psd_rate = Decimal(0.0698)
    vsd_rate = Decimal(0.1252)
    gpm_rate = Decimal(0.2)
    total_tax_rate = psd_rate + vsd_rate + gpm_rate
    post_tax_rate = 1 - total_tax_rate

    def calculate_pay(self, payment_amount, is_pay_net):
        if is_pay_net:
            return self.calculate_bruto(payment_amount)
        return self.calculate_neto(payment_amount)

    def calculate_neto(self, bruto):
        npd = self.npd_limit - Decimal(0.5) * (bruto - self.mma)
        psd = bruto * self.psd_rate
        vsd = bruto * self.vsd_rate
        gpm = (bruto - npd) * self.gpm_rate
        return self.format_amount(bruto - psd - vsd - gpm)

    def calculate_bruto(self, neto, pension_type="not_accumulate"):
        first_case_bruto = neto / (Decimal(0.805) - self.pension_rate[pension_type])
        if first_case_bruto <= self.npd_limit:
            return self.format_amount(first_case_bruto)

        second_case_bruto = (neto - Decimal(149.4)) / (
            self.post_tax_rate - self.pension_rate[pension_type]
        )
        if second_case_bruto <= self.mma:
            return self.format_amount(second_case_bruto)

        third_case_bruto = (neto - Decimal(241.8)) / (
            Decimal(0.505) - self.pension_rate[pension_type]
        )
        if third_case_bruto <= self.npd_bruto_limit:
            return self.format_amount(third_case_bruto)

        fourth_case_bruto = neto / self.post_tax_rate
        return self.format_amount(fourth_case_bruto)

    def format_amount(self, amount):
        return Decimal(amount).quantize(Decimal("0.00"))
