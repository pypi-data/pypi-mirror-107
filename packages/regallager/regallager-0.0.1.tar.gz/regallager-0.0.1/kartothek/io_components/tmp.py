import pandas as pd
import storefact
from functools import partial
from kartothek.io.eager import store_dataframes_as_dataset, read_dataset_as_dataframes

path = "/tmp"
uuid = "dataset"
df = pd.DataFrame({"a": [0, 0, 1, 1], "b": ["a", "a", "a", "b"], "c": [0, 0, 0, 0]})
store = partial(storefact.get_store_from_url, f"hfs://{path}?create_if_missing=False")
dm = store_dataframes_as_dataset(
    dfs=[df],
    dataset_uuid=uuid,
    store=store,
    partition_on=["a", "c"],
    overwrite=True,
)

df = read_dataset_as_dataframes(
    dataset_uuid=uuid, store=store, dispatch_by=["c"], categoricals={"table": ["b"]}
)
df[0]["table"].dtypes