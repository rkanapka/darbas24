from types import MappingProxyType


class Salary:
    pension_rate = MappingProxyType(
        {"not_accumulate": 0, "accumulateGradually": 0.027, "accumulate": 0.03}
    )
    mma = 924
    max_bruto = 2864.19

    npd_limit = 747
    npd_bruto_limit = 2167

    psd_rate = 0.0698
    vsd_rate = 0.1252
    gpm_rate = 0.2
    total_tax_rate = psd_rate + vsd_rate + gpm_rate
    post_tax_rate = 1 - total_tax_rate

    def calculate_neto(self, bruto):
        npd = self.npd_limit - 0.5 * (bruto - self.mma)
        psd = bruto * self.psd_rate
        vsd = bruto * self.vsd_rate
        gpm = (bruto - npd) * self.gpm_rate
        return bruto - psd - vsd - gpm

    def calculate_bruto(self, neto, pension_type="not_accumulate"):
        first_case_bruto = neto / (0.805 - self.pension_rate[pension_type])
        if first_case_bruto <= self.npd_limit:
            return first_case_bruto

        second_case_bruto = (neto - 149.4) / (
            self.post_tax_rate - self.pension_rate[pension_type]
        )
        if second_case_bruto <= self.mma:
            return second_case_bruto

        third_case_bruto = (neto - 241.8) / (0.505 - self.pension_rate[pension_type])
        if third_case_bruto <= self.npd_bruto_limit:
            return third_case_bruto

        fourth_case_bruto = neto / self.post_tax_rate
        return fourth_case_bruto
