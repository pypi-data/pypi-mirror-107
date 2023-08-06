from dataclasses import dataclass
from hashlib import sha256
from typing import List, Dict, Any


def quote_literal(text: str) -> str:
    "Escape the literal and wrap it in [single] quotations"
    return "'" + text.replace("'", "''") + "'"


def quote_ident(text: str) -> str:
    "Replace every instance of '" " with " "" " *and* place " "' on each end"
    return '"' + text.replace('"', '""') + '"'


@dataclass
class SimplePseudorandomiser:
    value_list: List[str]

    def as_sql(self, seed_column_name: str) -> str:
        values = ", ".join([quote_literal(value) for value in self.value_list])
        column_name = quote_ident(seed_column_name)
        return f"(ARRAY[{values}]::varchar[])[1 + ({column_name} % {len(self.value_list)})]"

    def as_python(self, *, seed_value: int) -> Any:
        return self.value_list[seed_value % len(self.value_list)]


name_randomiser = SimplePseudorandomiser(
    value_list=[
        "Andrew",
        "Federico",
        "Fraser",
        "Nick",
        "Oisin",
        "Richard",
        "Tom",
        "Tricia",
        "William",
        "Zoe",
    ]
)


@dataclass
class HashingPseudorandomiser:
    value_list: List[str]

    def as_sql(self, seed_column_name: str) -> str:
        values = ", ".join([quote_literal(value) for value in self.value_list])
        column_name = quote_ident(seed_column_name)
        return (
            f"(ARRAY[{values}]::varchar[])[1 + ("
            f"('x' || right(sha256({column_name})::text, 6))::bit(24)::int "
            "% {len(self.value_list)})]"
        )

    def as_python(self, *, seed_value: Any) -> Any:
        if isinstance(seed_value, bytes):
            seed_value_b = seed_value
        else:
            seed_value_b = str(seed_value).encode("utf-8")
        integer_seed = int(sha256(seed_value_b).hexdigest()[-6:], 16)
        return self.value_list[integer_seed % len(self.value_list)]


@dataclass
class Deidentifier:
    operations: Dict[str, SimplePseudorandomiser]

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
