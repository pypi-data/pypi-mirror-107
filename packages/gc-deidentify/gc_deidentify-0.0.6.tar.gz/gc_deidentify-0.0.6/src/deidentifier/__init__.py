from dataclasses import dataclass, field
from datetime import date, timedelta
from hashlib import sha256
from typing import List, Dict, Any, Literal, Protocol, Mapping, Match
import re
from .data import FIRST_NAMES, LAST_NAMES


def quote_literal(text: str) -> str:
    "Escape the literal and wrap it in [single] quotations"
    return "'" + text.replace("'", "''") + "'"


def quote_ident(text: str) -> str:
    "Replace every instance of '" " with " "" " *and* place " "' on each end"
    return '"' + text.replace('"', '""') + '"'


class Randomiser(Protocol):
    def for_sql(self, seed_column_name: str) -> str:
        """Build SQL to randomise this database column"""

    def for_python(self, *, seed_value: int) -> int:
        """return a random value based on the seed value"""


class Selector(Protocol):
    def as_sql(self, seed_column_name: str) -> str:
        """Build SQL to randomise this database column"""

    def as_python(self, *, seed_value: int, original_values: Mapping[str, Any]) -> Any:
        """return a random value based on the seed value"""


@dataclass
class SingleValueSelector:
    value: str

    def as_sql(self, seed_column_name: str) -> str:  # pylint: disable=unused-argument
        return quote_literal(self.value)

    def as_python(
        self,
        *,
        seed_value: int,  # pylint: disable=unused-argument
        original_values: Dict[str, Any],  # pylint: disable=unused-argument
    ) -> Any:
        return self.value


@dataclass
class SimplePseudorandomiser:
    @staticmethod
    def for_sql(seed_column_name: str) -> str:
        return quote_ident(seed_column_name)

    @staticmethod
    def for_python(*, seed_value: int) -> int:
        return seed_value


@dataclass
class SimpleSelector:
    """
    Select one of the random values from the list based on the seed
    """

    randomiser: Randomiser
    value_list: List[str]

    def as_sql(self, seed_column_name: str) -> str:
        values = ", ".join([quote_literal(value) for value in self.value_list])
        random = self.randomiser.for_sql(seed_column_name=seed_column_name)
        return f"(ARRAY[{values}]::varchar[])[1 + ({random} % {len(self.value_list)})]"

    def as_python(
        self,
        *,
        seed_value: int,
        original_values: Dict[str, Any],  # pylint: disable=unused-argument
    ) -> Any:
        random = self.randomiser.for_python(seed_value=seed_value)
        return self.value_list[random % len(self.value_list)]


@dataclass
class FormatterSelector:
    format_string: str

    sub_prefix = "' || "
    sub_suffix = " || '"

    @classmethod
    def replacer(cls, matchobj: Match[str]) -> str:
        col = matchobj.group(1)
        return cls.sub_prefix + quote_ident(col) + cls.sub_suffix

    def as_sql(self, seed_column_name: str) -> str:  # pylint: disable=unused-argument
        # this is ugly
        regex = re.compile(r"{([^}]+)}")
        subbed = regex.sub(self.replacer, self.format_string)
        if subbed.startswith(self.sub_prefix):
            subbed = subbed[len(self.sub_prefix) :]
        else:
            subbed = "'" + subbed
        if subbed.endswith(self.sub_suffix):
            subbed = subbed[: -len(self.sub_prefix)]
        else:
            subbed = subbed + "'"
        return subbed

    def as_python(
        self,
        *,
        seed_value: int,  # pylint: disable=unused-argument
        original_values: Dict[str, Any],  # pylint: disable=unused-argument
    ) -> Any:
        return self.format_string.format(**original_values)


@dataclass
class DateRangeSelector:
    """
    Select one of the random values from the list based on the seed
    """

    first_date: date
    last_date: date
    randomiser: Randomiser
    _n_days_in_range: int = field(init=False)

    def __post_init__(self) -> None:
        self._n_days_in_range = 1 + (self.last_date - self.first_date).days

    def as_sql(self, seed_column_name: str) -> str:
        random = self.randomiser.for_sql(seed_column_name=seed_column_name)
        first_date = self.first_date.strftime("%Y-%m-%d")
        return f"({first_date}::DATE + ({random} % {self._n_days_in_range}) * '1 day')"

    def as_python(
        self,
        *,
        seed_value: int,
        original_values: Dict[str, Any],  # pylint: disable=unused-argument
    ) -> Any:
        random = self.randomiser.for_python(seed_value=seed_value)
        return self.first_date + timedelta(days=(random % self._n_days_in_range))


@dataclass
class HashingRandomiser:
    @staticmethod
    def for_sql(seed_column_name: str) -> str:
        column_name = quote_ident(seed_column_name)
        return f"('x' || right(sha256({column_name}::BYTEA)::text, 6))::bit(24)::int"

    @staticmethod
    def for_python(*, seed_value: Any) -> Any:
        if isinstance(seed_value, bytes):
            seed_value_b = seed_value
        else:
            seed_value_b = str(seed_value).encode("utf-8")
        integer_seed = int(sha256(seed_value_b).hexdigest()[-6:], 16)
        return integer_seed


RandomiserStyle = Literal["simple", "hashing"]


@dataclass
class Deidentifier:
    operations: Dict[str, Selector]

    def build_sql_for_table(
        self, *, table_name: str, seed_column_name: str, column_mapping: Dict[str, str]
    ) -> str:
        # column_mapping: maps column name to operation key

        sets: List[str] = [
            f"{quote_ident(column_name)}="
            f"{self.operations[mapper].as_sql(seed_column_name=seed_column_name)}"
            for column_name, mapper in column_mapping.items()
        ]
        set_parts = ", ".join(sets)
        return f"UPDATE {quote_ident(table_name)} SET {set_parts};"

    def deidentify_dict(
        self, seed_key: str, key_mapping: Mapping[str, str], values: Dict[str, Any]
    ) -> Dict[str, Any]:
        return {
            k: self.operations[key_mapping[k]].as_python(
                seed_value=values[seed_key], original_values=values
            )
            if k in key_mapping
            else value
            for k, value in values.items()
        }


first_name = SimpleSelector(randomiser=HashingRandomiser(), value_list=FIRST_NAMES)

last_name = SimpleSelector(randomiser=HashingRandomiser(), value_list=LAST_NAMES)

scrubbed = SingleValueSelector(value="<scrubbed>")
dob = DateRangeSelector(
    first_date=date(1950, 1, 1),
    last_date=date(2000, 12, 31),
    randomiser=HashingRandomiser(),
)
email = FormatterSelector(format_string="{first_name}.{last_name}@fake.genesiscare.com")

"""
mobile_phone_randomiser = partial(
    Deidentifier.select_randomiser, value_list=["<scrubbed>"]
)
"""
