import pandas as pd
import streamlit as st
from datetime import date
from dataclasses import dataclass, field
from decimal import ROUND_HALF_UP, Decimal

D = Decimal
Q = D('0.01')

def number(x):
    """Coerce to Decimal safely (works for int/float/str/Decimal)."""
    return x if isinstance(x, Decimal) else D(str(x))

def dp2(x):
    """Quantize to 2 dp, bankers rounding avoided with HALF_UP if you prefer."""
    return number(x).quantize(Q, rounding=ROUND_HALF_UP)

def _safe_add_years(d: date, years: int) -> date:
    # handle Feb 29 to Feb 28 on non-leap years
    try:
        return d.replace(year=d.year + years)
    except ValueError:
        # fallback for Feb 29 -> Feb 28
        return d.replace(month=2, day=28, year=d.year + years)
    
def _age_at_date(birthdate: date, ref_date: date) -> int:
    age = ref_date.year - birthdate.year - (
        (ref_date.month, ref_date.day) < (birthdate.month, birthdate.day)
    )
    return age
    
@dataclass
class SettingsState:
    dob: date = date(1967, 6, 29)
    start_age: int | None = None
    end_age: int | None = 95
    plan_start: date | None = None
    plan_end: date | None = None
    state_pension_age: int | None = 67
    state_pension_current_amount: Decimal | None = field(default_factory=lambda: Decimal("11_973"))
    state_pension_annual_increase: Decimal | None = field(default_factory=lambda: Decimal("2.0"))
    inflation_rate: Decimal | None = field(default_factory=lambda: Decimal("3.0"))

    dob_changed_event: bool = False
    plan_dates_changed_event: bool = False
    start_age_changed_event: bool = False
    end_age_changed_event: bool = False

    pension_changed_event: bool = False
    inflation_rate_changed_event: bool = False
    monthly_changed_event: bool = False
    annual_changed_event: bool = False
    rental_changed_event: bool = False
    cash_changed_event: bool = False
    isa_changed_event: bool = False
    gia_changed_event: bool = False
    sipp_changed_event: bool = False

    monthly_income: Decimal | None = field(default_factory=lambda: Decimal("5_000"))
    annual_income: Decimal | None = field(default_factory=lambda: Decimal("60_000"))

    rental1_value: Decimal | None = field(default_factory=lambda: Decimal("421"))
    rental1_start: int | None = 58
    rental1_end: int | None = 59

    rental2_value: Decimal | None = field(default_factory=lambda: Decimal("300"))
    rental2_start: int | None = 58
    rental2_end: int | None = 95
    rent_increase: Decimal | None = field(default_factory=lambda: Decimal("2.0"))

    cash_value: Decimal | None = field(default_factory=lambda: Decimal("30_000"))
    cash_interest: Decimal | None = field(default_factory=lambda: Decimal("2.0"))

    isa_value: Decimal | None = field(default_factory=lambda: Decimal("200_000"))
    isa_growth: Decimal | None = field(default_factory=lambda: Decimal("4.0"))

    gia_value: Decimal | None = field(default_factory=lambda: Decimal("400_000"))
    gia_growth: Decimal | None = field(default_factory=lambda: Decimal("4.0"))

    sipp_value: Decimal | None = field(default_factory=lambda: Decimal("500_000"))
    sipp_growth: Decimal | None = field(default_factory=lambda: Decimal("4.0"))

    reducedIncome: pd.DataFrame = field(
        default_factory=lambda: pd.DataFrame(
            {
            "age": [70, 75, 80],
            "percentage": [10, 25, 40]
            }
        )
    )

    def __post_init__(self):
        """Runs automatically right after dataclass is created."""
        self.enforce()

    # Derived + rules
    def current_age(self, today: date | None = None) -> int:
        today = today or date.today()
        return today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
    
    @property
    def start_min(self) -> int: return 55
    @property
    def start_max(self) -> int: return 80

    def dob_on_change(self):
        self.dob_changed_event = True
        self.to_session()
    
    def dob_changed(self, dob):
        self.dob = dob
        self.plan_start = _safe_add_years(self.dob, int(self.start_age))
        self.plan_end = _safe_add_years(self.dob, int(self.end_age))
        st.session_state["plan_start"] = self.plan_start
        st.session_state["plan_end"] = self.plan_end
        self.dob_changed_event = False
        self.to_session()

    def plan_date_on_change(self):
        self.plan_dates_changed_event = True
        self.to_session()

    def plan_dates_changed(self, dob, start, end):
        self.dob = dob
        self.plan_start = start
        self.plan_end = end
        self.start_age = _age_at_date(dob, start)
        self.end_age = _age_at_date(dob, end)
        st.session_state["start_age"] = self.plan_start
        st.session_state["end_age"] = self.plan_end
        self.plan_dates_changed_event = False
     
        self.to_session()

    def start_age_on_change(self):
        self.start_age_changed_event = True
        self.to_session()

    def start_age_changed(self, new_age: int):
        new_age = int(new_age)
        self.start_age = new_age
        self.plan_start = _safe_add_years(self.dob, int(new_age))
        st.session_state["plan_start"] = self.plan_start
        self.start_age_changed_event = False
        self.to_session()

    def end_age_on_change(self):
        self.end_age_changed_event = True
        self.to_session()

    def end_age_changed(self, new_age):
        self.end_age = int(new_age)
        self.plan_end = _safe_add_years(self.dob, int(new_age))
        st.session_state["plan_end"] = self.plan_end
        self.end_age_changed_event = False
        self.to_session()   
    
    def on_pension_change(self):
        self.pension_changed_event = True
        self.to_session()

    def monthly_on_change(self):
        self.monthly_changed_event = True
        self.to_session()

    def pension_changed(self, new_age, new_pension, new_rate):
        self.state_pension_current_amount = dp2(new_pension)
        self.state_pension_age = int(new_age)
        self.state_pension_annual_increase = dp2(new_rate)
        self.pension_changed_event = False

    def monthly_changed(self, new_monthly: Decimal | float):
        m = dp2(new_monthly)

        self.monthly_income = m
        self.annual_income = dp2(m * 12)
        st.session_state["annual_income"] = self.annual_income
        self.monthly_changed_event = False
        self.to_session()

    def annual_on_change(self):
        self.annual_changed_event = True
        self.to_session()

    def annual_changed(self, new_annual: Decimal | float):
        a = dp2(new_annual)
        self.annual_income = a
        self.monthly_income = dp2(a / 12)
        st.session_state["monthly_income"] = self.monthly_income
        self.annual_changed_event = False
        self.to_session()
    
    def inflation_rate_on_change(self):
        self.inflation_rate_changed_event = True
        self.to_session()

    def inflation_rate_changed(self, new_rate):
        self.inflation_rate = dp2(new_rate)
        self.inflation_rate_changed_event = False
        self.to_session()

    def rental_on_change(self):
        self.rental_changed_event = True
        self.to_session()

    def rental_changed(self, new_value1, new_start1, new_end1, new_value2, new_start2, new_end2, new_increase):
        self.rental1_value = dp2(new_value1)
        self.rental1_start = int(new_start1)
        self.rental1_end = int(new_end1)
        self.rental2_value = dp2(new_value2)
        self.rental2_start = int(new_start2)
        self.rental2_end = int(new_end2)
        self.rent_increase = dp2(new_increase)
        self.rental_changed_event = False
        self.to_session()

    def cash_on_change(self):
        self.cash_changed_event = True
        self.to_session()

    def cash_changed(self, new_value, new_interest):
        self.cash_value = dp2(new_value)
        self.cash_interest = dp2(new_interest)
        self.cash_changed_event = False
        self.to_session()

    def isa_on_change(self):
        self.isa_changed_event = True
        self.to_session()

    def isa_changed(self, new_value, new_growth):
        self.isa_value = dp2(new_value)
        self.isa_growth = dp2(new_growth)
        self.isa_changed_event = False
        self.to_session()

    def gia_on_change(self):
        self.gia_changed_event = True
        self.to_session()

    def gia_changed(self, new_value, new_growth):
        self.gia_value = dp2(new_value)
        self.gia_growth = dp2(new_growth)
        self.gia_changed_event = False
        self.to_session()

    def sipp_on_change(self):
        self.sipp_changed_event = True
        self.to_session()

    def sipp_changed(self, new_value, new_growth):
        self.sipp_value = dp2(new_value)
        self.sipp_growth = dp2(new_growth)
        self.sipp_changed_event = False
        self.to_session()

    def normalized_start(self) -> int:
        """Default start_age to DOB age, clamped to [55, 80]."""
        base = self.current_age() + 1
        base = min(max(base, self.start_min), self.start_max)
        return base

    def enforce(self):
        """Ensure start/end obey rules."""
        # Start age
        if self.start_age is None:
            self.start_age = self.normalized_start()

        self.start_age = int(min(max(self.start_age, self.start_min), self.start_max))

        if self.plan_start is None:
            self.plan_start = _safe_add_years(self.dob, self.start_age)
        # End age depends on start
        end_min = self.start_age + 10
        end_max = 100
        if self.end_age is None:
            self.end_age = 95

        # Auto-bump end if now below min
        if self.end_age < end_min:
            self.end_age = end_min
        # Clamp to max
        self.end_age = int(min(self.end_age, end_max))

        if self.plan_end is None:
            self.plan_end = _safe_add_years(self.dob, self.end_age)

        if self.monthly_income is not None:
            self.monthly_income = dp2(self.monthly_income)
        if self.annual_income is not None:
            self.annual_income = dp2(self.annual_income)

        self.to_session()

    def to_session(self):
        st.session_state["settings_state"] = self

    @staticmethod
    def from_session() -> "SettingsState":
        if "settings_state" not in st.session_state:
            st.session_state["settings_state"] = SettingsState()
        return st.session_state["settings_state"]
    
    def apply_withdrawal_and_growth(self, start_value, shortfall, growth_rate):
        start_value = number(start_value)
        shortfall   = number(shortfall)
        growth_rate = number(growth_rate)

        if shortfall > 0:
            take_value = min(start_value, shortfall)
            shortfall -= take_value
        else:
            take_value = 0

        end_value    = dp2(start_value - take_value)
        growth_value = dp2(end_value * (growth_rate / number('100')))
        end_value    = dp2(end_value + growth_value)

        return shortfall, end_value, take_value, growth_value
    
    def _rental_for_age(self, age, start, end, initial_monthly, prev_monthly):
        """Monthly rental for a given year based on start/end and annual increase."""
        if age < start or age > end:
            return number('0')
        prev_monthly = number(prev_monthly)
        if prev_monthly == number('0'):
            return dp2(initial_monthly)
        return dp2(prev_monthly * (number('1') + (number(self.rent_increase) / number('100'))))
    
    def cashflow(self):
        inflation_rate = number(self.inflation_rate) / number('100')
        inflation = number('1') + inflation_rate

        reduction_factor_by_age = {
            int(self.reducedIncome["age"][i]):
                (number('100') - number(self.reducedIncome["percentage"][i])) / number('100')
            for i in range(len(self.reducedIncome["age"]))
        }

        ages = list(range(self.start_age, self.end_age + 1))
        dates = pd.date_range(start=self.plan_start, periods=len(ages), freq="12ME")

        # Output series
        income_needed, pension_income = [], []
        rental_income, rental1_income, rental2_income = [], [], []
        short, deficit = [], []

        sipp_start, sipp_take, sipp_growth, sipp_end = [], [], [], []
        gia_start, gia_take, gia_growth, gia_end = [], [], [], []
        isa_start, isa_take, isa_growth, isa_end = [], [], [], []
        cash_start, cash_take, cash_growth, cash_end = [], [], [], []

        prev_income = None
        prev_pension = 0.0
        prev_rental1 = 0.0
        prev_rental2 = 0.0

        # Starting balances
        current_gia = dp2(self.gia_value)
        current_isa = dp2(self.isa_value)
        current_sipp = dp2(self.sipp_value)
        current_cash = dp2(self.cash_value)
        current_deficit = dp2("0.00")

        for idx, age in enumerate(ages):
            # --- Income (annual) ---
            if idx == 0:
                income = dp2(self.annual_income)
            else:
                if age in reduction_factor_by_age:
                    base = dp2(self.annual_income) * (inflation ** (age - self.start_age))
                    income = base * dp2(reduction_factor_by_age[age])
                else:
                    income = prev_income * (1 + inflation_rate)

            # --- State pension (annual) ---
            if age < self.state_pension_age:
                pension = number(0.0)
            elif age == self.state_pension_age:
                pension = dp2(self.state_pension_current_amount)
            elif idx == 0:
                pension = dp2(self.state_pension_current_amount)
            else:
                pension = dp2(prev_pension * (1 + (dp2(self.state_pension_annual_increase) / number(100.0))))

            # --- Rentals (monthly -> annual) ---
            r1_month = self._rental_for_age(age, self.rental1_start, self.rental1_end, self.rental1_value, prev_rental1)
            r2_month = self._rental_for_age(age, self.rental2_start, self.rental2_end, self.rental2_value, prev_rental2)
            rental_annual = dp2((dp2(r1_month) + dp2(r2_month)) * number(12))

            # --- Net need / shortfall ---
            shortfall = income - pension - rental_annual

            # --- Draw from Cash then ISA ---
            gia_start_value = current_gia
            isa_start_value = current_isa
            sipp_start_value = current_sipp
            cash_start_value = current_cash

            shortfall, gia_end_value, gia_take_value, gia_growth_value = self.apply_withdrawal_and_growth(
                gia_start_value, shortfall, self.gia_growth
            )

            shortfall, isa_end_value, isa_take_value, isa_growth_value = self.apply_withdrawal_and_growth(
                isa_start_value, shortfall, self.isa_growth
            )
            shortfall, sipp_end_value, sipp_take_value, sipp_growth_value = self.apply_withdrawal_and_growth(
                sipp_start_value, shortfall, self.sipp_growth
            )

            shortfall, cash_end_value, cash_take_value, cash_growth_value = self.apply_withdrawal_and_growth(
                cash_start_value, shortfall, self.cash_interest
            )

            if shortfall < 0:
                cash_growth_value = cash_growth_value - shortfall
                cash_end_value = cash_end_value - shortfall
                shortfall = 0.0

            # --- Append outputs (rounded where appropriate) ---
            income_needed.append(float(round(income, 2)))
            pension_income.append(float(round(pension, 2)))
            rental_income.append(float(round(rental_annual, 2)))
            rental1_income.append(float(round(r1_month, 2)))
            rental2_income.append(float(round(r2_month, 2)))

            short.append(float(round(shortfall, 2)))

            gia_start.append(float(round(gia_start_value, 2)))
            gia_take.append(float(round(gia_take_value, 2)))
            gia_growth.append(float(round(gia_growth_value, 2)))
            gia_end.append(float(round(gia_end_value, 2)))

            isa_start.append(float(round(isa_start_value, 2)))
            isa_take.append(float(round(isa_take_value, 2)))
            isa_growth.append(float(round(isa_growth_value, 2)))
            isa_end.append(float(round(isa_end_value, 2)))

            sipp_start.append(float(round(sipp_start_value, 2)))
            sipp_take.append(float(round(sipp_take_value, 2)))
            sipp_growth.append(float(round(sipp_growth_value, 2)))
            sipp_end.append(float(round(sipp_end_value, 2)))

            cash_start.append(float(round(cash_start_value, 2)))
            cash_take.append(float(round(cash_take_value, 2)))
            cash_growth.append(float(round(cash_growth_value, 2)))
            cash_end.append(float(round(cash_end_value, 2)))


            # --- Carry forwards ---
            prev_income = income
            prev_pension = pension
            prev_rental1 = r1_month
            prev_rental2 = r2_month

            current_gia = gia_end_value
            current_isa = isa_end_value
            current_sipp = sipp_end_value
            current_cash = cash_end_value
            current_deficit = current_deficit - shortfall

            deficit.append(float(round(current_deficit, 2)))

        return pd.DataFrame(
            {
                "Date": dates.strftime("%Y"),
                "Age": ages,
                "Income": income_needed,
                "Pension": pension_income,
                "Rental": rental_income,
                "Short": short,
                "GIA Start": gia_start,
                "GIA Take": gia_take,
                "GIA Growth": gia_growth,
                "GIA End": gia_end,
                "ISA Start": isa_start,
                "ISA Take": isa_take,
                "ISA Growth": isa_growth,
                "ISA End": isa_end,
                "SIPP Start": sipp_start,
                "SIPP Take": sipp_take,
                "SIPP Growth": sipp_growth,
                "SIPP End": sipp_end,
                "Cash Start": cash_start,
                "Cash Take": cash_take,
                "Cash Growth": cash_growth,
                "Cash End": cash_end,
                "Deficit": deficit
            }, index=ages,
        )