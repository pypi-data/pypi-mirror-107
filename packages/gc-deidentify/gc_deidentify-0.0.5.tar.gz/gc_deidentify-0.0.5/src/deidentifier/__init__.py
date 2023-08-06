from dataclasses import dataclass
from functools import partial
from hashlib import sha256
from typing import List, Dict, Any, Literal, Protocol
from .data import FIRST_NAMES, LAST_NAMES


def quote_literal(text: str) -> str:
    "Escape the literal and wrap it in [single] quotations"
    return "'" + text.replace("'", "''") + "'"


def quote_ident(text: str) -> str:
    "Replace every instance of '" " with " "" " *and* place " "' on each end"
    return '"' + text.replace('"', '""') + '"'


class Randomiser(Protocol):
    def as_sql(self, seed_column_name: str) -> str:
        """Build SQL to randomise this database column"""

    def as_python(self, *, seed_value: int) -> Any:
        """return a random value based on the seed value"""


@dataclass
class SingleValueRandomiser:
    value: str

    def as_sql(self, seed_column_name: str) -> str:  # pylint: disable=unused-argument
        return quote_literal(self.value)

    def as_python(self, *, seed_value: int) -> Any:  # pylint: disable=unused-argument
        return self.value


@dataclass
class SimplePseudorandomiser:
    value_list: List[str]

    def as_sql(self, seed_column_name: str) -> str:
        values = ", ".join([quote_literal(value) for value in self.value_list])
        column_name = quote_ident(seed_column_name)
        return f"(ARRAY[{values}]::varchar[])[1 + ({column_name} % {len(self.value_list)})]"

    def as_python(self, *, seed_value: int) -> Any:
        return self.value_list[seed_value % len(self.value_list)]


@dataclass
class HashingPseudorandomiser:
    value_list: List[str]

    def as_sql(self, seed_column_name: str) -> str:
        values = ", ".join([quote_literal(value) for value in self.value_list])
        column_name = quote_ident(seed_column_name)
        return (
            f"(ARRAY[{values}]::varchar[])[1 + ("
            f"('x' || right(sha256({column_name}::BYTEA)::text, 6))::bit(24)::int "
            f"% {len(self.value_list)})]"
        )

    def as_python(self, *, seed_value: Any) -> Any:
        if isinstance(seed_value, bytes):
            seed_value_b = seed_value
        else:
            seed_value_b = str(seed_value).encode("utf-8")
        integer_seed = int(sha256(seed_value_b).hexdigest()[-6:], 16)
        return self.value_list[integer_seed % len(self.value_list)]


RandomiserStyle = Literal["simple", "hashing"]


@dataclass
class Deidentifier:
    operations: Dict[str, SimplePseudorandomiser]

    @staticmethod
    def select_randomiser(
        value_list: List[str], *, style: RandomiserStyle = "simple"
    ) -> Randomiser:
        if len(value_list) == 1:
            return SingleValueRandomiser(value=value_list[0])
        if style == "simple":
            return SimplePseudorandomiser(value_list=value_list)
        return HashingPseudorandomiser(value_list=value_list)

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
        self, seed_key: str, key_mapping: Dict[str, str], values: Dict[str, Any]
    ) -> Dict[str, Any]:
        return {
            k: self.operations[key_mapping[k]].as_python(seed_value=values[seed_key])
            if k in key_mapping
            else value
            for k, value in values.items()
        }


first_name_randomiser = partial(Deidentifier.select_randomiser, value_list=FIRST_NAMES)
last_name_randomiser = partial(Deidentifier.select_randomiser, value_list=LAST_NAMES)
